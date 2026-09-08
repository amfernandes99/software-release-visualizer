from release_data import load_releases


releases = load_releases("data/releases.csv")

for release in releases:
    print(
        release.release_id,
        release.name,
        release.release_date,
        release.stream,
        release.parent_id,
        release.status
    )
