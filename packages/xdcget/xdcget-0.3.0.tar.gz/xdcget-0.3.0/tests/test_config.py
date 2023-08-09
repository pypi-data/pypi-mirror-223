from pathlib import Path

import pytest
from xdcget.config import InvalidAppId, read_config, validate_app_id, write_xdcget_ini
from xdcget.errors import EmptyOrUnsetEnvVar, MissingOrEmptyField
from xdcget.main import main


class TestConfig:
    def test_init_and_read_config_basics(self, tmpdir, monkeypatch):
        # set some fake users and tokens to avoid configuration errors in read_config()
        for api in ["GITHUB", "CODEBERG"]:
            monkeypatch.setenv(f"XDCGET_{api}_USER", "test")
            monkeypatch.setenv(f"XDCGET_{api}_TOKEN", "test")

        tmpdir.chdir()
        main(["init"])
        config = read_config(Path("xdcget.ini"))
        assert config.export_dir == Path("export_dir").absolute()
        assert config.cache_dir == Path("cache_dir").absolute()
        cb = config.api_defs[0]
        assert cb.root_url == "https://codeberg.org"
        assert cb.api_url == "https://codeberg.org/api/v1/"
        gh = config.api_defs[1]
        assert gh.root_url == "https://github.com"
        assert gh.api_url == "https://api.github.com/"

    def test_read_config(self, tmpdir, monkeypatch):
        tmpdir.chdir()
        common_kwargs = dict(
            path=Path("xdcget.ini"),
            export_dir=Path("export_dir"),
            cache_dir=Path("cache_dir"),
        )

        write_xdcget_ini(
            **common_kwargs,
            codeberg_user_env_var="",
            codeberg_token_env_var="",
            github_user_env_var="",
            github_token_env_var="",
        )

        with pytest.raises(MissingOrEmptyField):
            read_config(common_kwargs["path"])

        write_xdcget_ini(
            **common_kwargs,
            codeberg_user_env_var="INVALID_CODEBERG_USER",
            codeberg_token_env_var="INVALID_CODEBERG_TOKEN",
            github_user_env_var="INVALID_GITHUB_USER",
            github_token_env_var="INVALID_GITHUB_TOKEN",
        )

        with pytest.raises(EmptyOrUnsetEnvVar):
            read_config(common_kwargs["path"])

        for api in ["github", "codeberg"]:
            monkeypatch.setenv(f"invalid_{api}_user".upper(), "test")
            monkeypatch.setenv(f"invalid_{api}_token".upper(), "test")

        read_config(common_kwargs["path"])

    def test_iter_xdc_sources(self, config_example1):
        xdc1, xdc2 = config_example1.iter_xdc_sources()
        assert xdc1.source_def.source_code_url == "https://github.com/webxdc/checklist"
        assert xdc1.source_def.app_id == "webxdc-checklist"
        assert xdc1.auth
        assert xdc2.source_def.source_code_url == "https://codeberg.org/webxdc/poll"
        assert xdc2.source_def.app_id == "webxdc-poll"
        assert xdc2.auth

    def test_latest_release_api_url(self, config_example1):
        repo1, repo2 = config_example1.iter_xdc_sources()
        assert (
            repo1.latest_release_api_url
            == "https://api.github.com/repos/webxdc/checklist/releases/latest"
        )
        assert (
            repo2.latest_release_api_url
            == "https://codeberg.org/api/v1/repos/webxdc/poll/releases/latest"
        )

    @pytest.mark.parametrize("app_id", ["A-b", "a-b-", "-a-b", "0a", "Aa", "a.b"])
    def test_app_id_fails(self, app_id):
        with pytest.raises(InvalidAppId):
            validate_app_id(app_id)

    @pytest.mark.parametrize("app_id", ["a", "a-b", "a-b-c", "a0", "a0-b"])
    def test_app_id_ok(self, app_id):
        validate_app_id(app_id)
