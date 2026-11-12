import shutil
from pathlib import Path

import pytest

from release_data import choose_release_date, load_releases

SAMPLE_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# Copies the sample data into a temporary folder so a test can change it safely
def copy_sample_data(tmp_path):
    data_dir = tmp_path / "data"
    shutil.copytree(SAMPLE_DATA_DIR, data_dir)
    return data_dir


# TEST 1 - The most reliable date is chosen: Received, Forecast, Due


def test_choose_release_date_priority():
    received = {
        "received_date": "2025-03-21",
        "forecast_date": "2025-03-14",
        "due_date": "2025-03-07",
    }
    forecast = {
        "received_date": "",
        "forecast_date": "2026-01-16",
        "due_date": "2025-12-26",
    }
    due_only = {"received_date": "", "forecast_date": "", "due_date": "2026-04-10"}

    assert str(choose_release_date(received)) == "2025-03-21"
    assert str(choose_release_date(forecast)) == "2026-01-16"
    assert str(choose_release_date(due_only)) == "2026-04-10"


# TEST 2 - The sample data loads, and the parent-child links come from relationships.csv


def test_sample_data_loads():
    releases = load_releases(SAMPLE_DATA_DIR)
    release_lookup = {release.release_id: release for release in releases}

    assert len(releases) == 37
    assert release_lookup["R027"].parent_id == "R003"


# TEST 3 - A release with an unknown stream is rejected rather than silently left off the chart


def test_unknown_stream_is_rejected(tmp_path):
    data_dir = copy_sample_data(tmp_path)
    releases_file = data_dir / "releases.csv"
    releases_file.write_text(
        releases_file.read_text().replace(",Main,Released,", ",Mian,Released,", 1)
    )

    with pytest.raises(ValueError, match="Unknown stream 'Mian'"):
        load_releases(data_dir)


# TEST 4 - A relationship pointing to a release that doesn't exist is rejected


def test_missing_parent_is_rejected(tmp_path):
    data_dir = copy_sample_data(tmp_path)

    with open(data_dir / "relationships.csv", "a") as relationships_file:
        relationships_file.write("R999,R002\n")

    with pytest.raises(ValueError, match="R999"):
        load_releases(data_dir)
