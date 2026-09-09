# Defining the Release class to represent a software release
class Release:
    def __init__(
            self,
            release_id,
            name, 
            release_date, 
            stream, 
            parent_id=None, 
            status="Planned",
            defects=0,
            changes=0,
            tests=0,
            integration_status="Not Applicable",
            component_version="Not Applicable"
            ):
        self.release_id = release_id
        self.name = name
        self.release_date = release_date
        self.stream = stream
        self.parent_id = parent_id
        self.status = status
        self.defects = defects
        self.changes = changes
        self.tests = tests
        self.integration_status = integration_status
        self.component_version = component_version
