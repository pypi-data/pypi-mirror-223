import oa_atomacos
import pytest


def test_get_app_ref_by_localized_name(finder_app):
    finder = oa_atomacos.getAppRefByLocalizedName("Finder")
    assert finder == finder_app


def test_get_bad_localized_name():
    with pytest.raises(ValueError):
        oa_atomacos.getAppRefByLocalizedName("Bad Localized Name")


def test_launch_app_by_bundle_path():
    oa_atomacos.launchAppByBundlePath("/Applications/Calculator.app")
    automator = oa_atomacos.getAppRefByLocalizedName("Calculator")
    assert automator.pid != 0


def test_set_systemwide_timeout():
    oa_atomacos.setSystemWideTimeout(0)


def test_get_app_by_bundle_id(finder_app):
    bid = finder_app.getBundleId()
    bybid = oa_atomacos.getAppRefByBundleId(bid)
    assert bybid == finder_app


def test_bad_bundle_id():
    with pytest.raises(ValueError):
        oa_atomacos.getAppRefByBundleId("bad.bundle.id")


def test_get_app_by_pid(finder_app):
    pid = finder_app.pid
    app = oa_atomacos.getAppRefByPid(pid)
    assert app == finder_app
