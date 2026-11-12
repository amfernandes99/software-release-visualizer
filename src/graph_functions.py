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

INTEGRATION_COLOURS = {
    "Ready": "tab:green",
    "Testing": "tab:orange",
    "In Development": "tab:blue",
    "Planned": "grey",
    "Not Applicable": "lightgrey",
}

STATUS_MARKERS = {
    "Released": "o",
    "Testing": "s",
    "Planned": "^",
}

# Calculate the y position based on the release stream
def calculate_y_position(release):
    return STREAM_POSITIONS.get(release.stream, 0)

# Creates an empty timeline page. One lane per stream, with months along the x-axis.
# Every page of the report starts from this.
def create_timeline_axes(title):
    fig, ax = plt.subplots(figsize=(16, 8))

    ax.set_yticks([3, 2, 1], ["Main", "Development", "Integration"])
    ax.set_ylim(0.8, 3.5)
    
    # Extra space on the right so the last labels aren't cut off
    ax.margins(x=0.08)

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))

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

# Draws an arrow from a parent release to its child.
# Links within a stream are straight, links between streams are grey, dashed, and curved.
def draw_release_link(ax, parent, child):
    if parent.stream == child.stream:       
        colour = STREAM_COLOURS.get(child.stream, "grey")
        line_style = "solid"
        connection = "arc3,rad=0"
    else:
        colour = "grey"
        line_style = "dashed"
        connection = "arc3,rad=0.2"

    ax.annotate(
        "",
        xy=(child.release_date, calculate_y_position(child)),
        xytext=(parent.release_date, calculate_y_position(parent)),
        arrowprops=dict(
            arrowstyle="-|>",
            color=colour,
            linestyle=line_style,
            linewidth=1.5,
            shrinkA=5,
            shrinkB=5,
            connectionstyle=connection, 
        ),
        zorder=1
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

        # Draws an arrow from the parent release to this release
        if release.parent_id:
            parent = release_lookup.get(release.parent_id)

            if parent:
                draw_release_link(ax, parent, release)

    # Legend for the release status, built from the same markers used on the chart
    legend_items = [
        Line2D([0], [0], marker=marker, color="w", markerfacecolor="grey",
               markersize=8, label=status)
        for status, marker in STATUS_MARKERS.items()
    ]
    ax.legend(handles=legend_items, loc="upper left", bbox_to_anchor=(1.01, 1))

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
        colour = INTEGRATION_COLOURS.get(release.integration_status, "grey")
        add_release_point(ax, release, label, colour=colour)

    # Legend for the integration status colours
    legend_items = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=colour,
               markersize=8, label=status)
        for status, colour in INTEGRATION_COLOURS.items()
    ]
    ax.legend(handles=legend_items, loc="upper left", bbox_to_anchor=(1.01, 1))

    fig.tight_layout()
    return fig

def create_core_components_graph(releases):
    fig, ax = create_timeline_axes("Core Components")

    for release in releases:
        label = f"{release.name}\n{release.component_version}"
        add_release_point(ax, release, label)

    fig.tight_layout()
    return fig