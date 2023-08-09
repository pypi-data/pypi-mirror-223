"""Command-line utility.

SPDX-License-Identifier: GPL-3.0-or-later
"""
import argparse
import hashlib
import logging
import pathlib
import shutil
import sys
from typing import Generator, List, Optional

from sextant import DEPFILE, RE_VERSION, dependency, log, module, scaffold
from sextant.semver import Semver


class ChartsCollection:
    """Manages a charts collection"""

    def __init__(self, modules_dir: str, charts_dir: str):
        self.registry = module.registry_from_path(modules_dir)
        self.path = pathlib.Path(charts_dir)

    def chart(self, chart_name: str) -> "Chart":
        """Fetches a specific chart"""
        pkgfile = self.path / chart_name / DEPFILE
        if not pkgfile.exists():
            raise KeyError(f"Could not find packagefile '{pkgfile}' chart '{chart_name}'")
        return Chart(self.registry, pkgfile)

    def charts(self) -> Generator["Chart", None, None]:
        """Returns all charts in the collection.

        This means all directories that are at the first level
        of the fs tree and contain a package.json file
        """
        for chartpath in self.path.rglob(DEPFILE):
            yield Chart(self.registry, chartpath)

    def query(self, query: str) -> List["Chart"]:
        """Query the chart collection for charts including a specific module."""
        self._check_query_format(query)
        results = []
        for chart in self.charts():
            try:
                if chart.depends_on(query):
                    results.append(chart)
            except dependency.DependencyError as exc:
                log.error("Chart %s has dependency problems: %s", chart, exc)
        return results

    def _check_query_format(self, query: str):
        # Check parameters
        try:
            base, _ = query.split(":")
            _, _ = base.split(".")
        except ValueError as exc:
            raise RuntimeError("The query needs to be in the format: namespace.module:version") from exc


class Chart:
    """Manages chart vendorization."""

    BUNDLE_DIR = "templates/vendor"

    def __init__(self, registry: module.Registry, packagefile: pathlib.Path):
        self.registry = registry
        self.chart_dir = packagefile.parent
        self.chart_yaml = self.chart_dir / "Chart.yaml"
        self.vendor_dir = self.chart_dir / self.BUNDLE_DIR
        self.package = dependency.Package(self.registry, str(packagefile))

    @classmethod
    def create(cls, registry: module.Registry, chartdir: str, scaffold_dir: str, presets: Optional[str]) -> "Chart":
        """Create a chart directory."""
        chart_dir = pathlib.Path(chartdir)
        if chart_dir.exists():
            raise ValueError(f"Directory {chartdir} exists.")
        if presets is not None:
            preset_file: Optional[pathlib.Path] = pathlib.Path(presets)
        else:
            preset_file = presets
        wizard = scaffold.ScaffoldWizard(chart_dir, pathlib.Path(scaffold_dir), preset_file=preset_file)
        packagefile = wizard.synth()
        return cls(registry, packagefile)

    def create_lock(self, force: bool):
        """Create a lockfile to freeze the dependencies."""
        self.package.lock(force)

    def _refresh_package(self):
        self.package = dependency.Package(self.registry, str(self.package.path))

    def vendor(self, force: bool, skip_version_bump: bool = False):
        """Creates a bundle of all modules required by the chart, and saves it
        to a vendor directory."""
        modified = False
        self.vendor_dir.mkdir(exist_ok=True)
        valid_targets: List[pathlib.Path] = []
        for mod in self.package.get(force):
            target = self.vendor_dir / mod.path.parent.name / mod.path.name
            target.parent.mkdir(exist_ok=True)
            valid_targets.append(target)
            if not force and self._is_fresh(target):
                log.debug("Not updating module %s as the its file is newer than the lockfile.", mod)
                continue
            if self._copy_if_changed(mod.path, target):
                modified = True
                log.info("Copied %s => %s", mod.path, target)

        # Now remove stale files
        for path in self.vendor_dir.glob("**/*.tpl"):
            if path in valid_targets:
                continue
            log.info("Pruning stale file %s", path)
            modified = True
            path.unlink()
        if modified and not skip_version_bump:
            self.bump_chart_version()

    def _is_fresh(self, target: pathlib.Path) -> bool:
        return target.exists() and self.package.lockfile.stat().st_mtime <= target.stat().st_mtime

    def _copy_if_changed(self, src: pathlib.Path, dst: pathlib.Path) -> bool:
        if dst.exists():
            src_md5sum = hashlib.md5(src.read_bytes()).hexdigest()
            dst_md5sum = hashlib.md5(dst.read_bytes()).hexdigest()
            if src_md5sum == dst_md5sum:
                log.debug("Not updating %s because it is unchanged", str(dst))
                return False
        shutil.copy(str(src), str(dst))
        return True

    def __str__(self) -> str:
        """String representation"""
        return self.chart_dir.name

    def depends_on(self, query: str, strict_match: bool = True) -> bool:
        """Checks if the chart depends on a module, directly or indirectly."""
        if strict_match:
            return any(str(m) == query for m in self.package.get())
        return any(m.matches(query) for m in self.package.get())

    def update_dependency(self, mod: module.Module) -> bool:
        """Update a dependency in package.json."""
        slug = f"{mod.namespace}.{mod.name}:{mod.version.major}.{mod.version.minor}"
        # If the update needs to happen in package.json, or if
        # we have an implicit dependency on it, force a re-vendoring.
        # Case 1: we have the module declared explicitly in package.json;
        # if the updated version is newer than the old one
        if self.package.update(slug):
            log.debug("Explicit dependency %s is newer than the one present in package.json", slug)
            return True
        # Case 2: we have the module imported as a dependency of another module.
        for dep_module in self.package.get():
            # Check that our update and the dependency are compatible.
            # If not, we can't update
            if not dep_module.matches(slug):
                continue
            # Now check that we are actually updating the module
            if mod.is_newer(dep_module):
                log.debug("Implicit dependency %s is newer than the current dependency %s", mod, dep_module)
                return True
        return False

    def bump_chart_version(self, specific_version="") -> Semver:
        """Bump the chart version after a vendor update."""
        with self.chart_yaml.open() as yaml:
            content = yaml.read()
        match = RE_VERSION.search(content)
        if not match:
            raise KeyError(f"Chart version could not be determined from {self.chart_yaml}")
        if specific_version != "":
            version = Semver(specific_version)
            cur_version = Semver(match[2])
            if version < cur_version:
                raise ValueError(
                    f"Chart version is currently '{cur_version}', which is newer than the requested '{version}'"
                )
        else:
            version = Semver(match[2])
            version.patch += 1
        content = RE_VERSION.sub(rf"\g<1>{str(version)}", content)
        with self.chart_yaml.open("w") as yaml:
            yaml.write(content)

        return version


def argparser():
    """Get the argument parser for the command line"""
    parser = argparse.ArgumentParser(prog="sextant", description="Tool to manage template libraries for helm charts")
    parser.add_argument("--modulepath", default="./modules", help="the directory where the modules are located.")
    parser.add_argument("--debug", action="store_true", help="output debug logging.")
    action = parser.add_subparsers(dest="action", required=True)
    # Command 1: bundle charts
    bundle = action.add_parser("vendor", help="allows to package your dependencies in a vendored file")
    bundle.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Re-create the lockfile and the bundle even if not necessary.",
    )
    bundle.add_argument(
        "--no-version-bump",
        "-b",
        action="store_true",
        help="Do not bump the chart version unless strictly necessary.",
    )
    bundle.add_argument(
        "chartdir",
        metavar="CHART_DIRECTORY",
        help="the directory where the chart's package.json file is located.",
    )
    # Command 2: search modules in charts
    search = action.add_parser(
        "search",
        help="search all charts in a directory for dependencies on a specific module",
    )
    search.add_argument("chartdir", metavar="CHARTS_DIRECTORY", help="the directory tree to search into")
    search.add_argument(
        "query",
        metavar="NAMESPACE.MODULE:VERSION",
        help="the module to search. WARNING: Only exact version matches for now.",
    )
    # Command 3: update a specific module to the latest version in the specified chart tree
    update = action.add_parser("update", help="update a module version across a directory of charts.")
    update.add_argument("chartdir", metavar="CHARTS_DIRECTORY", help="the directory tree to update into")
    update.add_argument("modules", metavar="MODULES", nargs="+")
    # Command 4: create a new  chart using our modules.
    create = action.add_parser("create-chart", help="Launches a wizard to create a new chart.")
    create.add_argument(
        "chartdir",
        metavar="CHART_DIRECTORY",
        help="the directory where the chart's package.json file is located.",
    )
    create.add_argument(
        "--scaffold", "-s", help="relative path to the scaffolding template.", default="_scaffold/sextant"
    )
    create.add_argument(
        "--presets", "-p", help="YAML file containing selections of components and answers", default=None
    )
    # Comand 5: change a chart version
    chart_version = action.add_parser("update-version", help="Updates the version of a chart")
    chart_version.add_argument(
        "--version", "-v", help="Optionally define a specific version to bump the chart to.", default=""
    )
    chart_version.add_argument(
        "chartdir",
        metavar="CHART_DIRECTORY",
        help="the directory where the chart's package.json file is located.",
    )
    return parser


def main(args: Optional[List[str]] = None):
    """The main entrypoint."""
    if args is None:
        args = sys.argv[1:]
    params = argparser().parse_args(args)
    if params.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    what = params.action.replace("-", "_")
    if what in ["vendor", "create_chart", "update_version"]:
        chartsdir = str(pathlib.Path(params.chartdir).parent)
    elif what is not None:
        chartsdir = params.chartdir

    charts = ChartsCollection(params.modulepath, chartsdir)

    try:
        handler = getattr(sys.modules[__name__], f"run_{what}")
        handler(params, charts)
    except Exception as exc:  # pylint: disable=W0703
        log.exception(exc)
        sys.exit(1)


def run_vendor(params: argparse.Namespace, charts: ChartsCollection):
    """Vendor dependencies."""
    chart_path = pathlib.Path(params.chartdir)
    charts.chart(chart_path.name).vendor(params.force, params.no_version_bump)


def run_create_chart(params: argparse.Namespace, charts: ChartsCollection):
    """Create a new chart"""
    chart = Chart.create(charts.registry, params.chartdir, params.scaffold, params.presets)
    print(f"Chart {chart} created, now vendoring dependencies.")
    chart.vendor(False, skip_version_bump=True)


def run_search(params: argparse.Namespace, charts: ChartsCollection):
    """Run search"""
    results = charts.query(params.query)
    if not results:
        print(f"The query for {params.query} returned no results.")
    else:
        print(f"Charts depending on the module {params.query}:")
        print()
        for chart in results:
            print(chart)


def run_update(params: argparse.Namespace, charts: ChartsCollection):
    """Perform the update action."""
    # First collect the modules to update
    updated_modules: List[module.Module] = []
    for mod in params.modules:
        try:
            namespace, module_name = mod.split(".", 1)
        except ValueError:
            log.error("Module names must be in the form 'namespace.module[:version]', got %s", mod)
            sys.exit(1)
        if ":" in module_name:
            module_name, version = module_name.split(":")
        else:
            version = None
        newest = charts.registry.get_newest(namespace=namespace, module=module_name, version=version)
        if newest is None:
            log.error("Could not find module '%s'", mod)
            sys.exit(1)
        log.info("Charts will be updated to %s", newest)
        updated_modules.append(newest)

    # Now update the dependencies in all charts.
    for chart in charts.charts():
        log.info("Updating %s...", chart)
        to_vendor = False
        for mod in updated_modules:
            log.debug("Checking updates to %s", mod)
            if chart.update_dependency(mod):
                to_vendor = True
        if to_vendor:
            log.info("Re-vendoring dependencies after update")
            chart.vendor(True)
        else:
            log.info("No update needed for chart %s", chart)


def run_update_version(params: argparse.Namespace, charts: ChartsCollection):
    """Bump chart version."""
    chart_path = pathlib.Path(params.chartdir)
    charts.chart(chart_path.name).bump_chart_version(params.version)
