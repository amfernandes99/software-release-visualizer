import csv

from models import Release


def load_releases(file_path):
    releases = []

    with open(file_path, newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            release = Release(
                row["release_id"],
                row["name"],
                row["release_date"],
                row["stream"],
                row["parent_id"] if row["parent_id"] else None,
                row["status"]
            )

            releases.append(release)

    return releases
