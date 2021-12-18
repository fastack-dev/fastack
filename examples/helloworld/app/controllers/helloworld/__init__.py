from fastack.controller import RetrieveController


class HelloWorldController(RetrieveController):
    # url_prefix = "/helloworld"

    def get(self):
        return self.json("Hello World!")

    def retrieve(self, id: int):
        return self.json("Detail hello world", {"id": id, "title": "hello world"})
