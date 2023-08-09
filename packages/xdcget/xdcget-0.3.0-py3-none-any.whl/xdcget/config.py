import configparser
import os
import re
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .errors import EmptyOrUnsetEnvVar, MissingOrEmptyField


@contextmanager
def line_writer(fn):
    with fn.open("w") as f:

        def writer(*args):
            print(*args, file=f)

        yield writer


def write_initial_config(xdcget_ini, out):
    assert not xdcget_ini.exists(), xdcget_ini
    write_xdcget_ini(
        xdcget_ini, export_dir=Path("export_dir"), cache_dir=Path("cache_dir")
    )
    out.green(f"created -- please inspect: {xdcget_ini}")


def write_xdcget_ini(
    path,
    export_dir,
    cache_dir,
    codeberg_user_env_var="XDCGET_CODEBERG_USER",
    codeberg_token_env_var="XDCGET_CODEBERG_TOKEN",
    github_user_env_var="XDCGET_GITHUB_USER",
    github_token_env_var="XDCGET_GITHUB_TOKEN",
    sources="""\
#[app:<projectname>]
#source_code_url =
##description =
""",
):
    def get_rel_or_abs(path, rootpath):
        path = path.absolute()
        rootpath = rootpath.absolute()
        if path.is_relative_to(rootpath.parent):
            return Path(path.relative_to(rootpath.parent))
        return path

    with line_writer(path) as w:
        cache_dir = get_rel_or_abs(cache_dir, path)
        export_dir = get_rel_or_abs(export_dir, path)

        w("[xdcget]")
        w("# all paths can be relative to the directory of the xdcget.ini file")
        w(f"export_dir = {export_dir}")
        w(f"cache_dir = {cache_dir}")
        w()
        w("[api:codeberg]")
        w("root_url = https://codeberg.org")
        w("api_url = https://codeberg.org/api/v1/")
        w(f"user_env_var = {codeberg_user_env_var}")
        w(f"token_env_var = {codeberg_token_env_var}")
        w()
        w("[api:github]")
        w("root_url = https://github.com")
        w("api_url = https://api.github.com/")
        w(f"user_env_var = {github_user_env_var}")
        w(f"token_env_var = {github_token_env_var}")
        w()
        w(sources)


def read_config(xdcget_ini_path):
    with xdcget_ini_path.open("r") as f:
        parser = configparser.ConfigParser()
        parser.read_file(f)
        api_defs = []
        app_defs = []
        cfg = None
        basedir = xdcget_ini_path.parent
        for key in sorted(parser.sections()):
            api_def = parser[key]
            if key.startswith("api:"):
                if not api_def.get("user_env_var"):
                    raise MissingOrEmptyField(section=key, field="user_env_var")
                if not api_def.get("token_env_var"):
                    raise MissingOrEmptyField(section=key, field="token_env_var")
                user = os.environ.get(api_def["user_env_var"])
                if not user:
                    raise EmptyOrUnsetEnvVar(section=key, var=api_def["user_env_var"])
                token = os.environ.get(api_def["token_env_var"])
                if not token:
                    raise EmptyOrUnsetEnvVar(section=key, var=api_def["token_env_var"])
                api_defs.append(
                    HostedApiDef(
                        api_def["root_url"], api_def["api_url"], user=user, token=token
                    )
                )
            elif key.startswith("app:"):
                app_id = key[len("app:") :]
                validate_app_id(app_id)
                app_defs.append(SourceDef(app_id=app_id, **parser[key]))
            else:
                assert key == "xdcget"
                cfg = parser[key]

    return Config(
        xdcget_ini_path=xdcget_ini_path,
        export_dir=basedir.joinpath(cfg["export_dir"]),
        cache_dir=basedir.joinpath(cfg["cache_dir"]),
        api_defs=api_defs,
        source_defs=app_defs,
    )


def validate_app_id(app_id):
    if app_id.lower() != app_id:
        raise InvalidAppId(f"{app_id!r} is not lowercase")
    rex = re.compile(r"^[a-z][a-z0-9\-]*$")
    if not rex.match(app_id) or app_id.strip("-") != app_id:
        raise InvalidAppId(f"{app_id!r} contains invalid characters")


class InvalidAppId(Exception):
    """Invalid app-id for a app."""


@dataclass
class HostedApiDef:
    root_url: str
    api_url: str
    user: str
    token: str

    @property
    def auth(self):
        return self.user, self.token

    def serves(self, api_def):
        return api_def.source_code_url.startswith(self.root_url)

    def get_current_rate_limit(self, requests):
        if self.root_url == "https://github.com":
            r = requests.get("https://api.github.com/rate_limit", auth=self.auth)
            r.raise_for_status()
            cr = r.json()["resources"]["core"]
            return "gh api rate limits: {} out of {}, reset in {} secs".format(
                cr["used"], cr["limit"], cr["reset"] - time.time()
            )


@dataclass
class SourceDef:
    app_id: str
    source_code_url: str
    description: Optional[str] = ""


@dataclass
class XDCSource:
    export_dir: Path
    source_def: SourceDef
    api_def: HostedApiDef

    @property
    def description(self):
        return self.source_def.description

    @property
    def latest_release_api_url(self):
        root_url = self.api_def.root_url
        sc = self.source_def.source_code_url
        assert sc.startswith(root_url)
        repo_and_name = sc[len(root_url) :].strip("/")
        if root_url == "https://codeberg.org":
            return f"https://codeberg.org/api/v1/repos/{repo_and_name}/releases/latest"
        elif root_url == "https://github.com":
            return f"https://api.github.com/repos/{repo_and_name}/releases/latest"

    @property
    def auth(self):
        return self.api_def.auth

    @property
    def app_id(self):
        return self.source_def.app_id


class Config:
    def __init__(self, xdcget_ini_path, export_dir, cache_dir, api_defs, source_defs):
        self.xdcget_ini_path = xdcget_ini_path
        basedir = xdcget_ini_path.parent
        self.export_dir = basedir.joinpath(export_dir).absolute()
        self.cache_dir = basedir.joinpath(cache_dir).absolute()
        self.api_defs = api_defs
        self.source_defs = source_defs

    @property
    def app_index_path(self):
        return self.xdcget_ini_path.parent.joinpath("xdcget.lock").absolute()

    def iter_xdc_sources(self):
        for source_def in self.source_defs:
            for api_def in self.api_defs:
                if api_def.serves(source_def):
                    yield XDCSource(self.export_dir, source_def, api_def)
                    break

    def get_xdc_source(self, app_id):
        for xdc_source in self.iter_xdc_sources():
            if xdc_source.app_id == app_id:
                return xdc_source
