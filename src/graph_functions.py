import matplotlib.pyplot as plt

# Setting up the parent-child relationships between releases
def set_release_relationships(releases):
    for release in releases:
        release.children = []

    for release in releases:
        if release.parent_id:
            for possible_parent in releases:
                if possible_parent.release_id == release.parent_id:
                    possible_parent.children.append(release)
                    break

# Creating x/y positions for the releases based on their release date and stream
# Calculate the x position based on the release date
def calculate_x_position(release, start_date):
    days_from_start = (release.release_date - start_date).days
    return days_from_start

# Calculate the y position based on the releases
def calculate_y_position(release):
    stream_positions = {
        "Main": 3,
        "Development": 2,
        "Integration": 1
    }

    return stream_positions.get(release.stream, 0)

# Visualising the release graph using matplotlib library
def create_release_graph(releases):
    start_date = min(release.release_date for release in releases)

    for release in releases:
        x_position = calculate_x_position(release, start_date)
        y_position = calculate_y_position(release)

        plt.scatter(x_position, y_position)
        plt.text(
            x_position,
            y_position + 0.1,
            release.name,
            ha="center"
        
        )

        if release.parent_id:
            for possible_parent in releases:
                if possible_parent.release_id == release.parent_id:
                    parent_x = calculate_x_position(possible_parent, start_date)
                    parent_y = calculate_y_position(possible_parent)

                    plt.plot(
                        [parent_x, x_position],
                        [parent_y, y_position]
                    )

                    break

    plt.xlabel("Days from first release")
    plt.ylabel("Release stream")
    plt.title("Software Release Overview")
    plt.show()
