import csv
from datetime import datetime
from models import Release


def load_releases(file_path):
    releases = []
    release_ids = set()

    with open(file_path, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
# Validation check to ensure that there are no duplicate release IDs in the CSV file. If a duplicate is found, a ValueError is raised with a message indicating the duplicate release ID.
        for row in reader:
            if row["release_id"] in release_ids:
                raise ValueError(f"Duplicate release ID: {row['release_id']}")

            release_ids.add(row["release_id"])            

            release = Release(
                row["release_id"],
                row["name"],
                datetime.strptime(row["release_date"], "%Y-%m-%d").date(),
                row["stream"],
                row["parent_id"] if row["parent_id"] else None,
                row["status"],
                int(row["defects"]),
                int(row["changes"]),
                int(row["tests"]),
                row["integration_status"],
                row["component_version"]
            )

            releases.append(release)

    return releases
