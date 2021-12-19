from fastapi import Request, status
from fastapi.responses import JSONResponse
from mongoengine import ValidationError, connect, disconnect_all

from fastack import Fastack


def handle_validation_error(request: Request, exc: ValidationError):
    content = {"detail": exc.message}
    return JSONResponse(content, status_code=status.HTTP_400_BAD_REQUEST)


def setup(app: Fastack):
    @app.on_event("startup")
    def on_startup():
        url = app.state.settings.MONGODB_URI
        connect(host=url)

    @app.on_event("shutdown")
    def on_shutdown():
        disconnect_all()

    app.add_exception_handler(ValidationError, handle_validation_error)
