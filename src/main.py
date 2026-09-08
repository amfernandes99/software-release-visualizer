from release_data import load_releases
from graph_functions import set_release_relationships, calculate_x_position, calculate_y_position, create_release_graph


releases = load_releases("data/releases.csv")

set_release_relationships(releases)
start_date = min(release.release_date for release in releases)

for release in releases:
    x_position = calculate_x_position(release, start_date)
    y_position = calculate_y_position(release)

    print(release.name, "-", x_position, y_position)

    for child in release.children:
        print("   ->", child.name)

create_release_graph(releases)
