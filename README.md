# Software Release Visualiser

A Python application for visualising software release timelines, relationships and release metadata.

The application reads release data from CSV, models relationships between software releases and generates a multi-page PDF report showing release progression across different development streams.

## Project Background

This project is an independent recreation inspired by software release visualisation work I have previously worked on professionally. The original tool processed release information from a company database and created a visual report in PDF format. I then presented this report to the wider organisation, including senior managers and colleagues with a less technical background.

This version was built from scratch using fictional release data and a simplified architecture, while retaining the core idea of turning software release information into a more user-friendly visual format.

## Features

- Loads and processes software release data from CSV format.
- Models parent-child relationships between releases.
- Visualises releases across multiple development streams and dates.
- Displays release status, defects, changes and testing information.
- Includes integration software status and component version information.
- Generates four visualisations within a single PDF report.
- Validates release data for duplicate IDs and missing parent relationships.

## Report Pages

The generated PDF contains four visualisations:

1. **Software Release Overview** - Displays the release timeline, development streams, release status and parent-child relationships between releases.
2. **Defects, Changes and Testing** - Displays defect, change and test information associated with each software release.
3. **Integration Software** - Displays the integration status associated with each release.
4. **Core Components** - Displays the component version associated with each release.

## Example Output

An example four-page report generated using the fictional release dataset is included in this repository:

`software_release_report.pdf`