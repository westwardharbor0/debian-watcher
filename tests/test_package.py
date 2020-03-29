from unittest import TestCase
from bs4 import BeautifulSoup

from debian_watcher.packages import Packages

BASE_URL = "https://packages.debian.org/"

EXPECTED_DETAIL_RESPONSE = {
    "stable": "1.2.3",
    "url": BASE_URL + "stable/libs/test_package",
    "name": "test_package",
    "distros": [
        {
            "name": "buster",
            "url": BASE_URL + "test/uri"
        }
    ]
}


class DetailPackages(Packages):
    @staticmethod
    def load_page_to_bs(id):
        html = """
            <div>
               <h1>{} ({})</h1> 
               <div id="pothers">
                    <a href="{}" >{}</a>
               </div>
            </div>
        """.format(
            EXPECTED_DETAIL_RESPONSE.get("name"), EXPECTED_DETAIL_RESPONSE.get("stable"),
            "/" + EXPECTED_DETAIL_RESPONSE["distros"][0].get("url").replace(BASE_URL, ""),
            EXPECTED_DETAIL_RESPONSE["distros"][0].get("name")
        )
        return BeautifulSoup(html, features="html.parser")


class DistrosPackages(Packages):
    def load_page_to_bs(id):
        html = """
            <div>
               <h1>{} ({})</h1>
            </div>
        """.format(id, "1.2.9")
        return BeautifulSoup(html, features="html.parser")


class TestDetail(TestCase):
    def test_detail(self):
        packages = DetailPackages()
        detail = packages.load_detail("test_package", distro_versions=False)
        assert detail == EXPECTED_DETAIL_RESPONSE


class TestDistros(TestCase):
    def test_distros(self):
        packages = DistrosPackages()
        distros = packages.load_distro_versions(EXPECTED_DETAIL_RESPONSE.get("distros"))
        expected_distros = EXPECTED_DETAIL_RESPONSE.get("distros")
        expected_distros[0].update({"version": "1.2.9"})
        assert distros == expected_distros
