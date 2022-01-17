# Plugin

Plugins in fastack are just python modules/packages which are imported in app build. All plugins can be added to the app via the `PLUGINS` configuration in the app settings. Then we'll look for the `setup()` function and then pass the app instance to the `setup()` function. So you can add anything to the app, like adding `startup` and `shutdown` events to initialize your plugin. See below...

## Create a plugin

Let's create a plugin for logging purposes

!!! note

    Plugins can be placed anywhere, but we recommend in the `app/plugins` folder

```py title="app/plugins/logger.py" linenums="1" hl_lines="7 16 17 19"
--8<-- "examples/helloworld/app/plugins/logger.py"
```

Lines:

* `7` - Get the `Logger` object. See line `19`.
* `16`, `17` - Set the logging level to DEBUG if the app is in debug mode.
* `19` - Set the `Logger` object to `app.state`, so we can make it globally accessible.

## Adding a plugin

Put the plugin into the `PLUGINS` configuration according to the settings of the app being used.

```py
PLUGINS = [
    ...,
    "app.plugins.logger",
]
```

## Test it

```py title="examples/helloworld/app/controllers/helloworld/__init__.py" linenums="1" hl_lines="2 20"
--8<-- "examples/helloworld/app/controllers/helloworld/__init__.py"
```

Lines:

* `2` - We import global logger object
* `20` - We print `Hello there!` if global variable `say_hello` is `True`.

The code above is taken from the [example project](https://github.com/fastack-dev/fastack/tree/main/examples/helloworld)
