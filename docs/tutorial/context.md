# Application Context

Application context here means, letting you access application instance object globally (like flask, if you've tried it). Example:

```py title="app/controllers/config.py"
from fastack import Controller
from fastack.globals import current_app

class ConfigController(Controller):
    def get(self, name: str):
        return self.json("Config", {"setting": name, "value": current_app.get_setting(name)})
```

Add the above controller into the app and if you send

```
curl -X 'GET' \
   'http://127.0.0.1:7874/config?name=DEBUG' \
   -H 'accept: application/json'
```

you will get

```json
{
  "detail": "Config",
  "data": {
    "setting": "DEBUG",
    "value": true
  }
}
```

!!! warning

    Never add controller above, it's dangerous because it will know the settings used by your application!

!!! note

    Local context can be used if:

    * Already running the app. Or...
    * Using `enable_context()` decorator.

## State

``state`` here is a shortcut for ``current_app.state`` which is used to store plugins in it. [See here](./plugins.md) for more details.


## How it works?

First, thanks to [werkzeug.local](https://werkzeug.palletsprojects.com/en/2.0.x/local/) for providing an API for object proxying.

It's simpler than you think (maybe :D). Basically a web framework is an object that can be called and accept requests that are forwarded by the web server.

This is the main point, we save the app object instance to local context using API from `contextvars.ContextVar` and also `werkzeug.local.LocalProxy` to access objects stored in local context.

For more details, please see the documentation directly:

* [werkzeug.local](https://werkzeug.palletsprojects.com/en/2.0.x/local/)
* [contextvars](https://docs.python.org/3/library/contextvars.html)
