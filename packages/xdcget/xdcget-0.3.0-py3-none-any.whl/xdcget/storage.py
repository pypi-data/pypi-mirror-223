"""Release caching and exporting of release files."""
import copy
import shutil
from contextlib import contextmanager
from dataclasses import dataclass
from zipfile import ZIP_DEFLATED, ZipFile

import requests
import toml


def do_request(url, auth=None, exc=True):
    r = requests.get(url, auth=auth)
    if exc and not r.ok:
        r.raise_for_status()
    return r


class NoReleases(Exception):
    def __init__(self, url):
        self.url = url


def get_latest_remote_release(xdcsource):
    r = do_request(xdcsource.latest_release_api_url, auth=xdcsource.auth, exc=False)
    if r.status_code == 404:
        raise NoReleases(xdcsource.latest_release_api_url)
    elif not r.ok:
        r.raise_for_status()

    json = r.json()
    tag_name = json["tag_name"]
    # we could look at lots of metadata in this json
    # but we just try grab the xdc file
    for asset in json["assets"]:
        name = asset["name"]
        if name.endswith(".xdc"):
            url = asset["browser_download_url"]
            date = asset["created_at"]
            return RemoteRelease(name, tag_name, url, date=date)


@dataclass
class RemoteRelease:
    name: str
    tag_name: str
    url: str
    date: str

    def download(self):
        r = do_request(self.url)
        r.raise_for_status()
        return r


def perform_update(config, app_filter, out, offline):
    """Update webxdcs.

    Args:
        config: configuration read from xdcget.ini
        app_filter: if not None, only update the sources
            whose app-id contains this string.
        out: output printer
        offline: if True, don't perform any network requests
    """
    if not offline:
        for api_def in config.api_defs:
            s = api_def.get_current_rate_limit(requests)
            if s:
                out(s)

    retrieved = changed = checked = num_all_problems = 0
    config.cache_dir.mkdir(exist_ok=True, parents=True)

    with app_index_writer(config=config) as app_index:
        for xdc_source in config.iter_xdc_sources():
            if app_filter and app_filter not in xdc_source.source_def.app_id:
                continue

            checked += 1
            if offline:
                index_release = app_index.get_release(xdc_source.app_id)
                remote_release = index_release
            else:
                try:
                    remote_release = get_latest_remote_release(xdc_source)
                except NoReleases as e:
                    out.red(f"NO RELEASES: {e.url}\n")
                    num_all_problems += 1
                    continue

                old = app_index.get_release(xdc_source.app_id)
                index_release = app_index.create_release_from_remote(
                    xdc_source.app_id, remote_release
                )
                if getattr(old, "tag_name", None) != index_release.tag_name:
                    changed += 1

            cache_path = config.cache_dir.joinpath(index_release.cache_relname)
            rel = index_release
            if True:
                s = f"got release: [{rel.app_id}] "
                s += " ".join([remote_release.name, rel.tag_name, rel.date])
                out(s)
                out(f"        url: {rel.url}")
            if cache_path.exists():
                out(f"     cached: {cache_path}")
            elif not offline:
                r = remote_release.download()
                cache_path.write_bytes(r.content)
                retrieved += 1
                out(f"     stored: {cache_path}", green=True)
            else:
                out.red("skipping download action because of offline run")
                out("")
                continue

            for problem in check_xdc_consistency(cache_path, xdc_source):
                out.red(problem)
                num_all_problems += 1

            manifest, _ = get_manifest_toml_and_icon(cache_path)
            index_release.name = manifest["name"]
            app_index.set_release(index_release)
            out("")

        out.green(f"{checked} apps checked from {config.app_index_path}")
        out.green(f"{changed} apps had newer versions")
        out.green(f"{retrieved} '.xdc' release files retrieved")
        if num_all_problems > 0:
            out.red(f"{num_all_problems} problems found")
        else:
            out.green("all good, no problems detected in .xdc files")


def check_xdc_consistency(xdc_path, xdc_source):
    """Check .xdc file. Yields found problems if any.

    Args:
        xdc_path: path to the .xdc file.
        xdc_source: corresponding part of the xdcget.ini source configuration file.
    """
    MAX_SUMMARY_CHARS = 30
    MIN_DETAILS_CHARS = 40

    manifest, icon_found = get_manifest_toml_and_icon(xdc_path)
    manifest_sc = manifest.get("source_code_url")
    if manifest_sc:
        sc = xdc_source.source_def.source_code_url
        if sc != manifest_sc:
            yield f"warn: manifest {manifest_sc} != {sc}"
    description = xdc_source.description
    if not description:
        yield "error: 'description' field not in xdcget.ini"
    else:
        lines = description.strip().split("\n")
        if len(lines[0]) > MAX_SUMMARY_CHARS:
            extra = len(lines[0]) - MAX_SUMMARY_CHARS
            yield f"error: description summary {extra} chars too much"
        if lines[0][-1:] == ".":
            yield "error: description summary ends with '.'"
        if len(lines) < 2:
            yield "error: description misses detail lines"
        else:
            joint = " ".join(lines[1:])
            if len(joint) < MIN_DETAILS_CHARS:
                yield "error: description details have less than 40 chars"

    if "app_id" in manifest:
        yield f"error: manifest has app_id {manifest['app_id']}, ignoring"
    if "version" in manifest:
        yield "error: manifest has 'version', ignoring"
    if not icon_found:
        yield "error: no 'icon.png' or 'icon.jpg' in .xdc file"


def get_manifest_toml_and_icon(xdc_path):
    """Extract manifest.toml from .xdc and check if it contains an icon."""
    zf = ZipFile(xdc_path)
    icon_found = manifest = None
    for fname in zf.namelist():
        if fname.lower().endswith("manifest.toml"):
            content = zf.read(fname)
            manifest = toml.loads(content.decode("utf-8"))
        elif fname.lower() in ("icon.png", "icon.jpg"):
            icon_found = True

    return manifest, icon_found


class IndexRelease:
    def __init__(
        self,
        app_id,
        tag_name,
        url,
        date,
        description,
        source_code_url="",
        name="",
    ):
        self.app_id = app_id
        self.tag_name = tag_name
        self.url = url
        self.date = date
        self.cache_relname = f"{app_id}-{tag_name}.xdc"
        self.description = description
        self.source_code_url = source_code_url
        self.name = name

    def __eq__(self, other):
        return self.__dict__ == getattr(other, "__dict__", None)

    def toml_data(self):
        return dict(
            app_id=self.app_id,
            name=self.name,
            tag_name=self.tag_name,
            url=self.url,
            date=self.date,
            cache_relname=f"{self.app_id}-{self.tag_name}.xdc",
            description=self.description,
            source_code_url=self.source_code_url,
        )


class AppIndex:
    """Application index."""

    def __init__(self, data, config):
        self._data = data  # Contents of the xdcget.lock file
        self.config = config  # Contents of the xdcget.ini file

    def get_num_apps(self):
        """Return number of applications in the index."""
        return len(self._data)

    def set_release(self, index_release: IndexRelease):
        assert "." not in index_release.app_id
        assert index_release.name, "name attribute can not be empty"
        self._data[index_release.app_id] = index_release.toml_data()

    def create_release_from_remote(self, app_id, remote_release):
        rel = remote_release
        source = self.config.get_xdc_source(app_id)
        return IndexRelease(
            app_id=app_id,
            tag_name=rel.tag_name,
            url=rel.url,
            date=remote_release.date,
            description=source.description,
            source_code_url=source.source_def.source_code_url,
        )

    def get_release(self, app_id):
        release = self._data.get(app_id)
        if release is not None:
            assert app_id == release["app_id"]
            if "cache_relname" in release:
                del release["cache_relname"]
            return IndexRelease(**release)

    def iter_releases(self):
        return (self.get_release(app_id) for app_id in self._data)


def get_app_index(config):
    """Read the application index.

    Args:
        config: contents of the xdcget.ini configuration file.
    """
    if config.app_index_path.exists():
        with config.app_index_path.open("r") as f:
            lock_data = toml.load(f)
    else:
        lock_data = {}
    return AppIndex(lock_data, config)


@contextmanager
def app_index_writer(config):
    path = config.app_index_path
    if path.exists():
        with path.open("r") as f:
            lock_data = toml.load(f)
    else:
        lock_data = {}
    new_data = copy.deepcopy(lock_data)

    # prune apps from the index not defined in our app sources list
    for app_id in set(new_data) - set(x.app_id for x in config.source_defs):
        del new_data[app_id]

    app_index = AppIndex(new_data, config=config)

    yield app_index

    if new_data != lock_data:
        tmp = path.parent.joinpath(path.name + ".tmp")
        with tmp.open("w") as f:
            toml.dump(new_data, f)
        tmp.rename(path)


def perform_export(config, out, offline):
    if config.export_dir.exists():
        shutil.rmtree(config.export_dir)

    config.export_dir.mkdir()
    app_index = get_app_index(config)
    num = 0
    for index_release in app_index.iter_releases():
        export_to_xdcstore(config, index_release)
        num += 1

    if num == 0:
        out.red("No apps to export, probably a configuration error?")
        raise SystemExit(1)

    dest = config.export_dir.joinpath(config.app_index_path.name)
    shutil.copy(config.app_index_path, dest)
    out.green(f"Exported store metadata for {num} apps to {dest}")
    out.green(f"Exported {num} webxdc release files to {dest.parent}")


def export_to_xdcstore(config, index_release):
    cache_path = config.cache_dir.joinpath(index_release.cache_relname)
    new_zf_path = config.export_dir.joinpath(index_release.cache_relname)
    # note that the original asset might use a different compression
    # method but we will write it out with standard ZIP_DEFLATED
    # because that's the only method that Delta Chat core supports as of 1.117.0
    zf = ZipFile(cache_path)
    new_zf = ZipFile(new_zf_path.open("wb"), compression=ZIP_DEFLATED, mode="w")
    for fname in zf.namelist():
        content = zf.read(fname)
        if fname == "manifest.toml":
            manifest = toml.loads(content.decode("utf-8"))
            # we know exactly where we were getting the source asset from
            # so it's a better source than what was manually specified
            manifest["source_code_url"] = index_release.source_code_url
            # put the "tag_name" into the produced manifest so that
            # together with the source_code_url we have a somewhat precise
            # reference for any ".xdc" file the store hands out
            manifest["tag_name"] = index_release.tag_name
            content = toml.dumps(manifest).encode("utf-8")
        new_zf.writestr(fname, data=content)
    new_zf.close()
    return new_zf_path
