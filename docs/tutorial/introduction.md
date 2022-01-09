# Introduction

This is the introduction section. How to create a project and an explanation of the application structure.

## Create a new project

```
fastack new your-project
```

## Application structure

We followed the project layout from the FastAPI documentation here https://fastapi.tiangolo.com/tutorial/bigger-applications/ with a few additions like changing the ``routers`` folder to ``controllers``.

```
$ tree your-project -I __pycache__
your-project
├── app
│   ├── commands
│   │   ├── __init__.py
│   │   └── user.py
│   ├── controllers
│   │   ├── dummy
│   │   │   ├── __init__.py
│   │   │   └── serializers.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── plugins
│   │   └── __init__.py
│   └── settings
│       ├── development.py
│       ├── __init__.py
│       ├── local.py
│       └── production.py
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── Pipfile
└── README.md
```

* ``app``: Location of your application
* ``app/commands``: A place to add your commands. [Want to jump?](./cli.md)
* ``app/controllers``: Location of REST APIs. [Want to jump?](./controller.md)
* ``app/main.py``: FastAPI App
* ``app/models.py``: A place to create (**Model** with *SQLModel*) or (**Document** with *MongoEngine*)
* ``app/plugins``: A place to make your own plugins. [Want to jump?](./plugins.md)
* ``app/settings``: Your app configuration list
* ``docker-compose.yml``, ``Dockerfile``, ``entrypoint.sh``: A file for bundling your app into a docker container.
* ``Pipfile``: We use ``pipenv`` as the package manager.
* ``README.md``: Short description to run your app

Now run your app:

```
cd your-project
fastack runserver
```

To run the app you can use the command ``fastack runserver`` or use ``uvicorn`` directly.

!!! warning

    Don't use ``fastack runserver`` in a production environment!

## Application settings

By default the app settings will use the local settings stored in ``app/settings/local.py``.
How do we use other settings? e.g. in a production environment.

To select the app settings for a specific environment, you can add the ``APP_ENV`` environment with a filename value that is in the ``app/settings`` directory. For example:

```sh
export APP_ENV=production
fastack runserver
```

It will use the settings from ``app/settings/production.py``. That's it :)
