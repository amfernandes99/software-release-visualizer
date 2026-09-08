import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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

    release_lookup = {
    release.release_id: release
    for release in releases
    }

    stream_colours = {
        "Main": "tab:blue",
        "Development": "tab:orange",
        "Integration": "tab:green"
    }

    status_markers = {
        "Released": "o",
        "Testing": "s",
        "Planned": "^"
    }

    for release in releases:
        x_position = release.release_date
        y_position = calculate_y_position(release)

        plt.scatter(
            x_position,
            y_position,
            s=60,
            color=stream_colours.get(release.stream, "grey"),
            marker=status_markers.get(release.status, "o"),
            zorder=3
        )

        plt.text(
            x_position,
            y_position + 0.08,
            release.name,
            ha="center"
        
        )

# Draws lines between parent and child releases, grabs parent directly by id
        if release.parent_id:
            parent = release_lookup.get(release.parent_id)

            if parent:
                parent_x = parent.release_date
                parent_y = calculate_y_position(parent)

                plt.plot(
                    [parent_x, x_position],
                    [parent_y, y_position],
                    color=stream_colours.get(release.stream, "grey"),
                    linewidth=1.5,
                    zorder=1
                )

    plt.yticks(
    [1, 2, 3],
    ["Integration", "Development", "Main"])

    plt.ylim(0.8, 3.4)


# Gets current axis and sets the x-axis to display months and years
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

    plt.xlabel("Release Date")
    plt.ylabel("Release Stream")
    plt.title("Software Release Overview")
    plt.show()
