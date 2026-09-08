class Release:
    def __init__(self, release_id, name, release_date, stream, parent_id=None, status="Planned"):
        self.release_id = release_id
        self.name = name
        self.release_date = release_date
        self.stream = stream
        self.parent_id = parent_id
        self.status = status
