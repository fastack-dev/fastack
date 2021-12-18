from fastack.controller import RetrieveController


class DummyController(RetrieveController):
    url_prefix = "/dummy"

    def retrieve(self, id: int):
        return self.json("Detail dummy", {"id": id, "title": "dummy"})
