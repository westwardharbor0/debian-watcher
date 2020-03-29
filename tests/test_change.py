from unittest import TestCase

from debian_watcher.change import Change

ACTUAL_STATE = '{"name": "tp", "url": "htts://url/tp", "stable": "0.0.23.1", "distros": [{"url": "htts://url/jessie/0ad", "name": "jessie", "version": "17"}]}'
HISTORY_STATE = '{"name": "tp", "url": "htts://url/tp", "stable": "0.0.23.1", "distros": [{"url": "htts://url/jessie/0ad", "name": "jessie", "version": "17"}]}'

class TestChange(TestCase):
    def test_no_changes(self):
        def _reporter(**kwargs):
            print(kwargs)
            raise Exception("There should not be changes")
        Change("tp", ACTUAL_STATE, HISTORY_STATE, _reporter).check_all()

    def test_distro_version_change(self):
        def _reporter(**kwargs):
            assert kwargs.get("from_version") == "17"
            assert kwargs.get("to_version") == "18"
        Change("tp", ACTUAL_STATE.replace("17", "18"), HISTORY_STATE, _reporter).check_all()

    def test_distro_added(self):
        _ACTUAL_STATE = '{"name": "tp", "url": "htts://url/tp", "stable": "0.0.23.1", "distros": [{"url": "htts://url/jessie/0ad", "name": "jessie", "version": "17"}, {"url": "htts://url/buster/0ad", "name": "buster", "version": "17"}]}'
        def _reporter(**kwargs):
            assert "Added" in kwargs.get("message")
            assert kwargs.get("distros") == ["buster"]
        Change("tp", _ACTUAL_STATE, HISTORY_STATE, _reporter).check_all()

    def test_distro_removed(self):
        _ACTUAL_STATE = '{"name": "tp", "url": "htts://url/tp", "stable": "0.0.23.1", "distros": []}'

        def _reporter(**kwargs):
            assert "Removed" in kwargs.get("message")
            assert kwargs.get("distros") == ["jessie"]

        Change("tp", _ACTUAL_STATE, HISTORY_STATE, _reporter).check_all()


