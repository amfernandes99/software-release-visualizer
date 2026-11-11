import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.lines import Line2D

# Shared chart settings, used by every page of the report.
# Each stream gets its own horizontal lane; a higher number is higher up the chart.
STREAM_POSITIONS = {
    "Main": 3,
    "Development": 2,
    "Integration": 1,
}

STREAM_COLOURS = {
    "Main": "tab:blue",
    "Development": "tab:orange",
    "Integration": "tab:green",
}

STATUS_MARKERS = {
    "Released": "o",
    "Testing": "s",
    "Planned": "^",
}

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

# Calculate the y position based on the release stream
def calculate_y_position(release):
    return STREAM_POSITIONS.get(release.stream, 0)

# Creates an empty timeline page. One lane per stream, with months along the x-axis.
# Every page of the report starts from this.
def create_timeline_axes(title):
    fig, ax = plt.subplots(figsize=(16, 8))

    ax.set_yticks([3, 2, 1], ["Main", "Development", "Integration"])
    ax.set_ylim(0.8, 3.5)

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

    ax.set_xlabel("Release Date")
    ax.set_ylabel("Release Stream")
    ax.set_title(title)

    return fig, ax

# Draws one release on the chart: a point in its lane, with its label just above
def add_release_point(ax, release, label, colour="grey", marker="o", fontsize=7):
    x_position = release.release_date
    y_position = calculate_y_position(release)

    ax.scatter(x_position, y_position, s=60, color=colour, marker=marker, zorder=3)

    ax.text(
        x_position,
        y_position + 0.08,
        label,
        ha="left",
        rotation=35,
        fontsize=fontsize
    )

def create_software_release_overview(releases):
    fig, ax = create_timeline_axes("Software Release Overview")

    release_lookup = {release.release_id: release for release in releases}

    for release in releases:
        add_release_point(
            ax,
            release,
            release.name,
            colour=STREAM_COLOURS.get(release.stream, "grey"),
            marker=STATUS_MARKERS.get(release.status, "o"),
            fontsize=8
        )

        # Draws a line from the parent release to this release
        if release.parent_id:
            parent = release_lookup.get(release.parent_id)

            if parent:
                ax.plot(
                    [parent.release_date, release.release_date],
                    [calculate_y_position(parent), calculate_y_position(release)],
                    color=STREAM_COLOURS.get(release.stream, "grey"),
                    linewidth=1.5,
                    zorder=1
                )

    # Legend for the release status, built from the same markers used on the chart
    legend_items = [
        Line2D([0], [0], marker=marker, color="w", markerfacecolor="grey",
               markersize=8, label=status)
        for status, marker in STATUS_MARKERS.items()
    ]
    ax.legend(handles=legend_items, loc="upper right")

    fig.tight_layout()
    return fig


def create_defects_changes_testing_graph(releases):
    fig, ax = create_timeline_axes("Defects, Changes and Testing")

    for release in releases:
        label = (
            f"{release.name}\n"
            f"D:{release.defects} C:{release.changes} T:{release.tests}"
        )
        add_release_point(ax, release, label)

    fig.text(
        0.5,
        0.02,
        "D = Defects    C = Changes    T = Tests",
        ha="center",
        fontsize=8
    )

    fig.tight_layout(rect=[0, 0.04, 1, 1])
    return fig

def create_integration_software_graph(releases):
    fig, ax = create_timeline_axes("Integration Software")

    for release in releases:
        label = f"{release.name}\n{release.integration_status}"
        add_release_point(ax, release, label)

    fig.tight_layout()
    return fig

def create_core_components_graph(releases):
    fig, ax = create_timeline_axes("Core Components")

    for release in releases:
        label = f"{release.name}\n{release.component_version}"
        add_release_point(ax, release, label)

    fig.tight_layout()
    return fig