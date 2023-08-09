import os
import sys

import pytest
import xdcget
from xdcget.main import get_parser, main


class TestCmdline:
    def test_parser(self, capsys):
        parser = get_parser()
        parser.parse_args([])
        init = parser.parse_args(["init"])
        update = parser.parse_args(["update"])
        assert init and update

    def test_init(self, tmpdir):
        tmpdir.chdir()
        main(["init"])
        assert tmpdir.join("xdcget.ini").exists()

    def test_no_args_description(self, capsys):
        with pytest.raises(SystemExit) as excinfo:
            main([])
        assert excinfo.value.code == 0
        out, err = capsys.readouterr()
        assert "Collect webxdc" in out
        assert " init " in out and "Initialize config" in out

    def test_version(self, capsys):
        with pytest.raises(SystemExit) as excinfo:
            main(["--version"])
        assert excinfo.value.code == 0
        out, err = capsys.readouterr()
        assert out.strip() == xdcget.__version__

    def test_init_not_overwrite(self, tmpdir):
        tmpdir.chdir()
        main(["init"])
        with pytest.raises(SystemExit):
            main(["init"])

    def test_update_from_different_dir(self, config_example1, tmp_path):
        p = tmp_path.joinpath("somewhere")
        p.mkdir()
        os.chdir(p)
        main(["--config", "../xdcget.ini", "update"])

    def test_prune_app_index(self, iniconfig):
        iniconfig.add_source(
            app_id="webxdc-poll",
            source_code_url="https://codeberg.org/webxdc/poll",
        )
        iniconfig.add_lock_entry(
            app_id="webxdc-poll",
            name="Poll",
            tag_name="v1.0.1",
            url="https://codeberg.org/attachments/d53543bd-d805-4aba-926d-88eefc7a9eef",
            date="2023-07-05T20:30:48Z",
            cache_relname="webxdc-poll-v1.0.1.xdc",
        )
        iniconfig.add_lock_entry(
            app_id="webxdc-checklist",
            name="Checklist",
            tag_name="v0.0.2",
            url="https://codeberg.org/attachments/65d05b8d-a97c-4fb6-a534-e308c382f874",
            date="2023-07-07T18:05:19Z",
            cache_relname="webxdc-checklist-v0.0.2.xdc",
        )

        config = iniconfig.create()
        assert "webxdc-poll" in config.app_index_path.read_text()
        assert "webxdc-checklist" in config.app_index_path.read_text()
        main(["update"])
        assert "webxdc-poll" in config.app_index_path.read_text()
        assert "webxdc-checklist" not in config.app_index_path.read_text()

    def test_update_empty(self, iniconfig):
        iniconfig.create()
        with pytest.raises(SystemExit):
            main(["update"])

    def test_update_no_network(self, capfd, config_example1, monkeypatch):
        main(["update"])
        p = config_example1.export_dir.joinpath("xdcget.lock")
        assert p.exists()
        assert len(p.read_text()) > 50
        monkeypatch.delattr(sys.modules["requests"], "get")
        main(["update", "--offline"])
