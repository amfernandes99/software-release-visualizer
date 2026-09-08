from release_data import load_releases
from graph_functions import set_release_relationships


releases = load_releases("data/releases.csv")

set_release_relationships(releases)

for release in releases:
    print(release.name)

    for child in release.children:
        print("   ->", child.name)
