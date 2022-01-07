from werkzeug.local import LocalStack

_app_ctx_stack = LocalStack()
_request_ctx_stack = LocalStack()
_websocket_ctx_stack = LocalStack()
