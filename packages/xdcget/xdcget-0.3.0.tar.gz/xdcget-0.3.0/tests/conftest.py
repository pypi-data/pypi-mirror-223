import io
import os
import zipfile

import pytest
import requests_mock
from xdcget.config import read_config, write_xdcget_ini


class RequestMocker:
    def __init__(self, mock):
        self.requests_mock = mock
        self.requests_mock.get(
            "https://api.github.com/rate_limit",
            json={
                "resources": {
                    "core": {
                        "limit": 5000,
                        "used": 44,
                        "remaining": 4956,
                        "reset": 1690891414,
                    }
                }
            },
        )

    def mock_source(self, url):
        url, owner, name = url.strip("/").rsplit("/", 2)
        gh_assets = [
            {
                "name": f"{name}.xdc",
                "created_at": "2023-07-05T20:30:48Z",
                "browser_download_url": f"https://mocker.com/attachments/{owner}/{name}.xdc",
            }
        ]
        if url.startswith("https://codeberg.org"):
            self.requests_mock.get(
                f"https://codeberg.org/api/v1/repos/{owner}/{name}/releases/latest",
                json={"tag_name": "v1.0.1", "assets": gh_assets},
            )
        elif url.startswith("https://github.com"):
            self.requests_mock.get(
                f"https://api.github.com/repos/{owner}/{name}/releases/latest",
                json={"tag_name": "v1.0.1", "assets": gh_assets},
            )

        self.requests_mock.get(
            f"https://mocker.com/attachments/{owner}/{name}.xdc",
            content=self._webxdc_content(name="poll"),
        )

    @staticmethod
    def _webxdc_content(name):
        xdc = io.BytesIO()
        with zipfile.ZipFile(xdc, "w", compression=zipfile.ZIP_DEFLATED) as fzip:
            fzip.writestr("manifest.toml", f'name = "{name}"')
            fzip.writestr("index.html", "test")
        xdc.seek(0)
        return xdc.read()


def pytest_addoption(parser):
    parser.addoption(
        "--online",
        action="store_true",
        help="run test online doing network access, if not provided, network"
        " connections will be mocked and tests will run offline.",
    )


@pytest.fixture
def requests_mocker(request):
    assert not request.config.getoption("--online")
    for api in ["GITHUB", "CODEBERG"]:
        os.environ[f"XDCGET_{api}_USER"] = "fakeuser"
        os.environ[f"XDCGET_{api}_TOKEN"] = "faketoken"
    with requests_mock.Mocker() as m:
        yield RequestMocker(m)


class IniConfig:
    def __init__(self, path, mocker=None):
        self._path = path
        self._mocker = mocker
        self.export_dir = path.joinpath("export_dir")
        self.cache_dir = path.joinpath("cache_dir")
        self.xdcget_ini_path = path.joinpath("xdcget.ini")
        self._sources = []
        self._locks = []

    def add_source(self, app_id, source_code_url, description=None):
        """Add a new app source to the xdcget configuration."""
        if description is None:
            description = "some desc\n  qlwkeqlwkelqwkelqwkelqkwleqkwleqkwle "
        self._sources.append(
            f"""
[app:{app_id}]
source_code_url = {source_code_url}
description = {description}
"""
        )
        if self._mocker is not None:
            self._mocker.mock_source(source_code_url)

    def add_lock_entry(
        self, app_id, name, tag_name, url, date, cache_relname, description=None
    ):
        """Add a new (pseudo) lock file entry to the xdcget configuration."""
        if description is None:
            description = "some desc\nqlwkeqlwkelqwkelqwkelqkwleqkwleqkwle"
        self._locks.append(
            f"""
[{app_id}]
app_id = "{app_id}"
name = "{name}"
tag_name = "{tag_name}"
url = "{url}"
date = "{date}"
cache_relname = "{cache_relname}"
description = "{description!r}"
"""
        )

    def create(self):
        """Create .ini and .lock files according to added sources/lock entries."""
        kw = dict(sources="\n".join(self._sources)) if self._sources else {}

        write_xdcget_ini(
            self.xdcget_ini_path,
            export_dir=self.export_dir,
            cache_dir=self.cache_dir,
            **kw,
        )
        if self._locks:
            with self._path.joinpath("xdcget.lock").open("w") as f:
                f.write("\n".join(self._locks))

        os.chdir(self._path)
        return read_config(self.xdcget_ini_path)


@pytest.fixture
def iniconfig(request, tmp_path):
    """Return helper object to create .ini/.lock files for xdcget.

    On the returned object you can call `add_source` and
    `add_lock_entry` multiple times before calling `create()`
    which will then write out .ini/.lock files accordingly
    and change the working directory to the directory containing the files.
    """
    if request.config.getoption("--online"):
        mocker = None
    else:
        mocker = request.getfixturevalue("requests_mocker")
    return IniConfig(tmp_path, mocker=mocker)


@pytest.fixture
def config_example1(iniconfig):
    iniconfig.add_source(
        app_id="webxdc-checklist",
        source_code_url="https://github.com/webxdc/checklist",
    )
    iniconfig.add_source(
        app_id="webxdc-poll", source_code_url="https://codeberg.org/webxdc/poll"
    )
    return iniconfig.create()
