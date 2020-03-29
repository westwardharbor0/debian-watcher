from requests import get
from bs4 import BeautifulSoup
from json import dumps
from logging import info, warning, error, basicConfig, INFO
from .change import Change


class Packages(object):
    def __init__(
            self, base_url="https://packages.debian.org",
            storage=None, reporter=None, logfile=None):
        self._base_url = base_url
        self._package_list_url = base_url + "/stable/allpackages"
        self._package_detail_url = base_url + "/stable/libs/{}"
        self._storage = storage
        self._reporter = reporter
        basicConfig(filename=logfile, level=INFO)

    @staticmethod
    def parse_version(title):
        return title.split("(")[1].replace(")", "").strip()

    @staticmethod
    def load_page_to_bs(url):
        return BeautifulSoup(get(url).text, features="html.parser")

    @classmethod
    def load_distro_versions(cls, distros):
        for distro in distros:
            url = distro.get("url")
            detail = cls.load_page_to_bs(url)
            distro["version"] = cls.parse_version(detail.find("h1").text)
        return distros

    def load_detail(self, id, distro_versions=True):
        url = self._package_detail_url.format(id)
        detail = self.load_page_to_bs(url)
        stable_version = self.parse_version(detail.find("h1").text)
        distros = self.load_detail_distros(detail)
        if distro_versions:
            distros = self.load_distro_versions(distros)
        return {
            "name": id,
            "url": url,
            "stable": stable_version,
            "distros": distros
        }

    def load_detail_distros(self, detail):
        ds = detail.find(id="pothers").find_all("a")
        return [{
            "url": self._base_url + d.get("href"),
            "name": d.text
        } for d in ds]

    def _check_package(self, id):
        detail = self.load_detail(id)
        actual_state = dumps(detail)
        last_state = self._storage.load_last_state(id)
        if last_state:
            if actual_state == last_state:
                info("Check {} - passed".format(id))
            else:
                warning(
                    "Check {} - failed (there are changes)".format(id))
                Change(
                    name=id,
                    actual=actual_state,
                    history=last_state,
                    custom_reporter=self._reporter
                ).check_all()
                self._storage.store_state(id, actual_state)

    def check_list(self, packages):
        info("Starting check_list")
        le = len(packages)
        for i, package in enumerate(packages):
            info("{}/{} Checking {}".format(i, le, package))
            self._check_package(package)
        info("Checking finished")

    def check_all(self):
        info("Starting check_all")
        info("Loading list of all packages")
        list_html = self.load_page_to_bs(self._package_list_url)
        packages = list_html.find_all("dt")
        info("Loaded packages list")
        le = len(packages)
        for i, package in enumerate(packages):
            href = package.find_all("a")[0]
            name = href.get("id")
            info("{}/{} Checking {}".format(i, le, name))
            self._check_package(name)
            i += 1
            if i > 40:
                break
        info("Checking finished")


