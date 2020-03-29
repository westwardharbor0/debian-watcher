
from os import listdir, mkdir, remove
from os.path import exists
from logging import info

from .cached import Cached


class Storage(Cached):
    def __init__(self, storage_dir=None, cache=True, max_history=20):
        if not storage_dir:
            raise Exception("Need to set storage dir")
        self._storage_dir = storage_dir
        self._cache_enabled = cache
        self._max_history = max_history

    @staticmethod
    def _filename(name):
        from datetime import datetime
        now = datetime.now().strftime("%m%d%Y_%H%M%S")
        return "{}_{}.json".format(name, now)

    def _remove_max_history(self, files, name):
        path = self._storage_dir + name
        for file in files[self._max_history - 1:]:
            info("Removing useless history {}".format(file))
            remove(path + "/" + file)

    def _list_files(self, name):
        path = self._storage_dir + name + "/"
        if not exists(path):
            mkdir(path)
        ls = listdir(path)
        ls = sorted(ls, reverse=True)
        if len(ls) > self._max_history:
            self._remove_max_history(ls, name)
        return ls

    @Cached._cache_result
    def load_history(self, name):
        return self._list_files(name)

    @Cached._cache_result
    def load_last_record(self, name):
        ls = self._list_files(name)
        return ls[0] if ls else ""

    def load_last_state(self, name):
        fn = self.load_last_record(name)
        if not fn:
            return ""
        return self.load_state(name, fn)

    def load_state(self, name, filename):
        path = self._storage_dir + name + "/"
        with open(path + filename, "r") as f:
            return f.read()

    def store_state(self, name, content):
        path = self._storage_dir + name + "/"
        if not exists(path):
            mkdir(path)
        with open(path + self._filename(name), "w+") as f:
            f.write(content)
