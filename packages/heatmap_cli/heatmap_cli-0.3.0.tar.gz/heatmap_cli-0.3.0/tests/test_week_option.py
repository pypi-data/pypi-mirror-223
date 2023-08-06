# pylint: disable=missing-module-docstring,missing-function-docstring

import pytest


@pytest.mark.parametrize("option", ["-wk", "--week"])
def test_debug_logs(cli_runner, csv_file, option):
    csv = csv_file("sample.csv")
    ret = cli_runner(f"{csv} -d {option} 42")

    assert "2023_week_42_RdYlGn_r__annotated_heatmap_" in ret.stdout
    assert "week=42" in ret.stdout


def test_last_week_of_the_year(cli_runner, csv_file):
    csv = csv_file("sample.csv")
    ret = cli_runner(f"{csv} -d -wk 52")

    assert "2023_RdYlGn_r__annotated_heatmap_" in ret.stdout
    assert "week=52" in ret.stdout
