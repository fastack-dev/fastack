from fastack import create_app
from tests import settings

app = create_app(settings)


@app.post("/api/test")
def api_test():
    return "api test"
