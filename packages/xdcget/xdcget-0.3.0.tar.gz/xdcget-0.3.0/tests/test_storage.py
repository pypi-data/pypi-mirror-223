import pytest
from xdcget.config import SourceDef, XDCSource
from xdcget.storage import RemoteRelease, app_index_writer, get_latest_remote_release


class TestAppIndex:
    @pytest.fixture
    def pseudo_Config(self):
        class Config:
            def __init__(self, path, app_ids=[]):
                self.app_index_path = path
                self.app_ids = app_ids
                self.source_defs = []

            def get_xdc_source(self, app_id):
                return XDCSource("", SourceDef("hello", "", ""), None)

        return Config

    def test_write_one(self, tmp_path, pseudo_Config):
        path = tmp_path.joinpath("test.lock")
        remote_release = RemoteRelease("hello", "0.1.0", "https://a.org", "DATE")

        config = pseudo_Config(path)
        with app_index_writer(config) as app_index:
            ir = app_index.create_release_from_remote("webxdc-hello", remote_release)
            ir.name = "hello"
            app_index.set_release(ir)

        assert app_index.get_release(app_id="xzy") is None
        assert app_index.get_num_apps() == 1
        release = app_index.get_release(app_id="webxdc-hello")
        assert release.url == remote_release.url
        assert release.tag_name == remote_release.tag_name
        assert release.name == "hello"
        assert release.cache_relname == "webxdc-hello-0.1.0.xdc"
        assert release == app_index.get_release(app_id="webxdc-hello")

        app_index.set_release(release)
        release2 = app_index.get_release("webxdc-hello")
        assert release2.cache_relname == release.cache_relname
        assert release2.tag_name == release.tag_name

    def test_write_three(self, tmp_path, pseudo_Config):
        path = tmp_path.joinpath("test.lock")
        config = pseudo_Config(path)
        with app_index_writer(config) as app_index:
            for num in range(4):
                rel = RemoteRelease("hello", f"0.{num}.0", "https://a.org", "DATE")
                ir = app_index.create_release_from_remote("webxdc-hello", rel)
                ir.name = "hello"
                app_index.set_release(ir)

        index_rel = app_index.get_release("webxdc-hello")
        assert index_rel.tag_name == "0.3.0"
        assert index_rel.url == "https://a.org"

        rel = RemoteRelease("hello", index_rel.tag_name, index_rel.url, "DATE")
        index_release = app_index.create_release_from_remote(index_rel.app_id, rel)
        assert index_release.tag_name == index_rel.tag_name


def test_get_latest_remote_release(config_example1):
    xdc1, xdc2 = config_example1.iter_xdc_sources()

    rel = get_latest_remote_release(xdc1)
    assert rel.name == "checklist.xdc"
    assert rel.tag_name
    assert rel.url
    assert rel.date

    rel = get_latest_remote_release(xdc2)
    assert rel.name == "poll.xdc"
    assert rel.tag_name
    assert rel.url
    assert rel.date
