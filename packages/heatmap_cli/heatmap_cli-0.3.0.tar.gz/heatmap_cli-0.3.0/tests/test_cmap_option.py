# pylint: disable=missing-module-docstring,missing-function-docstring

import pytest


@pytest.mark.parametrize("option", ["-cm", "--cmap"])
def test_debug_logs(cli_runner, csv_file, option):
    csv = csv_file("sample.csv")
    ret = cli_runner(f"{csv} -d {option} autumn")
    assert "cmap='autumn'" in ret.stdout


def test_default_cmap(cli_runner, csv_file):
    csv = csv_file("sample.csv")
    ret = cli_runner(f"{csv} -d")
    assert "cmap='RdYlGn_r'" in ret.stdout
