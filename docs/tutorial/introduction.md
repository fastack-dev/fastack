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
* ``app/commands``: A place to add your commands. [See here](./cli.md)
* ``app/controllers``: Location of REST APIs. [See here](./controller.md)
* ``app/main.py``: FastAPI App
* ``app/models.py``: A place to create model with SQLModel or document with mongoengine
* ``app/plugins``: A place to make your own plugins. [See here](./plugins.md)
* ``app/settings``: Your app configuration list
* ``docker-compose.yml``, ``Dockerfile``, ``entrypoint.sh``: A file for bundling your app into a docker container.
* ``Pipfile``: We use ``pipenv`` as the package manager.
* ``README.md``: Short description to run your app

Now run your app:

```
cd your-project
fastack runserver
```

!!! note

    To run the app you can use the command ``fastack runserver`` or use ``uvicorn`` directly.

And taraaa you just finished the introduction part, keep it up! 🥳
