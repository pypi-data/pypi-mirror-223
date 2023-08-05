class Installation:
    def __init__(self, data):
        self._installation_id = data["installation_id"]
        self._name = data["name"]
        self._description = data["description"]
        self._address = data["metadata"]["address"]
        self._status = data["status"]

    @property
    def installation_id(self):
        return self._installation_id

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def address(self):
        return self._address

    @property
    def status(self):
        return self._status
