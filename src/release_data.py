import csv
from datetime import datetime
from models import Release

# The only streams and statuses the report knows how to draw
VALID_STREAMS = ["Main", "Development", "Integration"]
VALID_STATUSES = ["Released", "Testing", "Planned"]

# Reads a CSV file into a list of rows, each row a dictionary keyed by column name
def read_csv(file_path):
    with open(file_path, newline="") as csv_file:
        return list(csv.DictReader(csv_file))


# Picks the most reliable date for a release: received, then forecast, then due
def choose_release_date(row):
    for column in ["received_date", "forecast_date", "due_date"]:
        if row[column]:
            return datetime.strptime(row[column], "%Y-%m-%d").date()

    return None

def load_releases(data_dir):
    release_rows = read_csv(data_dir / "releases.csv")
    relationship_rows = read_csv(data_dir / "relationships.csv")
    quality_rows = read_csv(data_dir / "quality.csv")
    integration_rows = read_csv(data_dir / "integration.csv")

    # Lookups so each release's details can be found by its ID
    parents = {row["child_id"]: row["parent_id"] for row in relationship_rows}
    quality = {row["release_id"]: row for row in quality_rows}
    integration = {row["release_id"]: row["integration_status"] for row in integration_rows}

    releases = []
    release_ids = set()

    for row in release_rows:
        release_id = row["release_id"]

        if release_id in release_ids:
            raise ValueError(f"Duplicate release ID: {release_id}")

        release_ids.add(release_id)

        if row["stream"] not in VALID_STREAMS:
            raise ValueError(f"Unknown stream '{row['stream']}' for release {release_id}")

        if row["status"] not in VALID_STATUSES:
            raise ValueError(f"Unknown status '{row['status']}' for release {release_id}")        

        release_date = choose_release_date(row)

        if release_date is None:
            raise ValueError(f"No received, forecast or due date for release {release_id}")

        release_quality = quality.get(release_id, {})

        release = Release(
            release_id,
            row["name"],
            release_date,
            row["stream"],
            parents.get(release_id),
            row["status"],
            int(release_quality.get("defects", 0)),
            int(release_quality.get("changes", 0)),
            int(release_quality.get("tests", 0)),
            integration.get(release_id, "Not Applicable"),
            row["component_version"]
        )

        releases.append(release)


    # Every parent and child in relationships.csv must be a known release
    for row in relationship_rows:
        for column in ["parent_id", "child_id"]:
            if row[column] not in release_ids:
                raise ValueError(f"Release {row[column]} in relationships.csv not found in releases.csv")

    return releases
