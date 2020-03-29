from json import loads
from logging import info, warning


class Change(object):
    def __init__(self, name="", actual="", history="", custom_reporter=None):
        self._package = name
        self._actual_state = loads(actual)
        self._history_state = loads(history)
        self._reporter = custom_reporter or self._report_problem

    @staticmethod
    def _report_problem(**kwargs):
        warning(kwargs)

    def check_all(self):
        self.check_distros_count()
        self.check_distros_versions()
        self.check_stable()
        self.check_dependecies()

    def check_distros_count(self):
        def _d_names(ls):
            return [l.get("name") for l in ls]
        ad = _d_names(self._actual_state.get("distros"))
        hd = _d_names(self._history_state.get("distros"))
        if ad != hd:
            ds = ad[:]
            ds.extend(hd)
            new_packages = list(set(ds) - set(hd))
            removed_packages = list(set(ds) - set(ad))
            if new_packages:
                self._reporter(
                    message="Added support for new distros",
                    distros=new_packages,
                    package=self._package
                )
            if removed_packages:
                self._reporter(
                    message="Removed support for distros",
                    distros=removed_packages,
                    package=self._package
                )

    def check_distros_versions(self):
        info("Checking ds")
        ads = self._actual_state.get("distros")
        hds = self._history_state.get("distros")
        for i, ad in enumerate(ads):
            if i > len(hds) - 1:
                continue
            if (
                ad.get("name") == hds[i].get("name") and
                ad.get("version") != hds[i].get("version")
            ):
                self._reporter(
                    message="Version for distro changed",
                    from_version=hds[i].get("version"),
                    to_version=ad.get("version"),
                    package=self._package,
                    distro=ad.get("name")
                )

    def check_stable(self):
        ads = self._actual_state.get("stable")
        hds = self._history_state.get("stable")
        if ads != hds:
            self._reporter(
                message="Version for stable changed",
                from_version=hds,
                to_version=ads,
                package=self._package
            )

    def check_dependecies(self):
        # TODO: in future updates add dependencies check
        pass
