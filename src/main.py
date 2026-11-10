import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from release_data import load_releases
from graph_functions import (
    set_release_relationships,
    create_software_release_overview,
    create_defects_changes_testing_graph,
    create_integration_software_graph,
    create_core_components_graph,
)

# Build paths from this file's location so the script runs from any folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate a PDF report showing software releases across development streams."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=PROJECT_ROOT / "data",
        help="Folder containing the release CSV files (default: data/)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "software_release_report.pdf",
        help="Where to save the PDF report (default: software_release_report.pdf)",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    releases = load_releases(args.data_dir / "releases.csv")
    set_release_relationships(releases)

    figures = [
        create_software_release_overview(releases),
        create_defects_changes_testing_graph(releases),
        create_integration_software_graph(releases),
        create_core_components_graph(releases),
    ]

    with PdfPages(args.output) as pdf:
        for figure in figures:
            pdf.savefig(figure)
            plt.close(figure)

    print(f"Report generated: {args.output}")


if __name__ == "__main__":
    main()
