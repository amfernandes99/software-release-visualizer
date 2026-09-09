from release_data import load_releases
from graph_functions import set_release_relationships, calculate_x_position, calculate_y_position, create_software_release_overview, create_defects_changes_testing_graph, create_integration_software_graph, create_core_components_graph
from matplotlib.backends.backend_pdf import PdfPages

releases = load_releases("data/releases.csv")

set_release_relationships(releases)
start_date = min(release.release_date for release in releases)

## Development check to verify release positioning and relationships.
# for release in releases:
#     x_position = calculate_x_position(release, start_date)
#     y_position = calculate_y_position(release)

#     print(
#         release.name,
#         "-",
#         release.defects,
#         "defects,",
#         release.changes,
#         "changes,",
#         release.tests,
#         "tests"
#     )

#     for child in release.children:
#         print("   ->", child.name)

overview_figure = create_software_release_overview(releases)
quality_figure = create_defects_changes_testing_graph(releases)
integration_figure = create_integration_software_graph(releases)
components_figure = create_core_components_graph(releases)

with PdfPages("software_release_report.pdf") as pdf:
    pdf.savefig(overview_figure)   
    pdf.savefig(quality_figure)
    pdf.savefig(integration_figure)
    pdf.savefig(components_figure)

print("Report generated: software_release_report.pdf")