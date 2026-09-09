import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
from matplotlib.backends.backend_pdf import PdfPages

# Setting up the parent-child relationships between releases
def set_release_relationships(releases):
    for release in releases:
        release.children = []

    for release in releases:
        if release.parent_id:
            parent_found = False
            
            for possible_parent in releases:
                if possible_parent.release_id == release.parent_id:
                    possible_parent.children.append(release)
                    parent_found = True
                    break

            if not parent_found:
                raise ValueError(
                    f"Parent release {release.parent_id} not found for {release.release_id}"
                )

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
def create_software_release_overview(releases):

    plt.figure(figsize=(16, 8))

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
            ha="left",
            rotation=35,
            fontsize=8            
        
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

# Legend for the release status
    legend_items = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor="grey",
            markersize=8, label="Released"),
        Line2D([0], [0], marker="s", color="w", markerfacecolor="grey",
            markersize=8, label="Testing"),
        Line2D([0], [0], marker="^", color="w", markerfacecolor="grey",
            markersize=8, label="Planned")
    ]

    plt.legend(handles=legend_items, loc="upper right")




    plt.tight_layout()
    return plt.gcf()


def create_defects_changes_testing_graph(releases):
    plt.figure(figsize=(16, 8))

    for release in releases:
        x_position = release.release_date
        y_position = calculate_y_position(release)

        plt.scatter(
            x_position,
            y_position,
            s=60,
            color="grey",
            zorder=3
        )

        release_info = (
            f"{release.name}\n"
            f"D:{release.defects} "
            f"C:{release.changes} "
            f"T:{release.tests}"
        )

        plt.text(
            x_position,
            y_position + 0.08,
            release_info,
            ha="left",
            rotation=35,
            fontsize=7
        )

    plt.yticks(
        [1, 2, 3],
        ["Integration", "Development", "Main"]
    )

    plt.ylim(0.8, 3.5)

    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter("%b %Y")
    )

    plt.xlabel("Release Date")
    plt.ylabel("Release Stream")
    plt.title("Defects, Changes and Testing")
    plt.figtext(
        0.5,
        0.02,
        "D = Defects    C = Changes    T = Tests",
        ha="center",
        fontsize=8
    )

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    return plt.gcf()

def create_integration_software_graph(releases):
    plt.figure(figsize=(16, 8))

    for release in releases:
        x_position = release.release_date
        y_position = calculate_y_position(release)

        plt.scatter(
            x_position,
            y_position,
            s=60,
            color="grey",
            zorder=3
        )

        integration_info = (
            f"{release.name}\n"
            f"{release.integration_status}"
        )

        plt.text(
            x_position,
            y_position + 0.08,
            integration_info,
            ha="left",
            rotation=35,
            fontsize=7
        )

    plt.yticks(
        [1, 2, 3],
        ["Integration", "Development", "Main"]
    )

    plt.ylim(0.8, 3.5)

    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter("%b %Y")
    )

    plt.xlabel("Release Date")
    plt.ylabel("Release Stream")
    plt.title("Integration Software")

    plt.tight_layout()
    return plt.gcf()

def create_core_components_graph(releases):
    plt.figure(figsize=(16, 8))

    for release in releases:
        x_position = release.release_date
        y_position = calculate_y_position(release)

        plt.scatter(
            x_position,
            y_position,
            s=60,
            color="grey",
            zorder=3
        )

        component_info = (
            f"{release.name}\n"
            f"{release.component_version}"
        )

        plt.text(
            x_position,
            y_position + 0.08,
            component_info,
            ha="left",
            rotation=35,
            fontsize=7
        )

    plt.yticks(
        [1, 2, 3],
        ["Integration", "Development", "Main"]
    )

    plt.ylim(0.8, 3.5)

    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter("%b %Y")
    )

    plt.xlabel("Release Date")
    plt.ylabel("Release Stream")
    plt.title("Core Components")

    plt.tight_layout()
    return plt.gcf()