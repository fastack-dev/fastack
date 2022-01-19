# Fastack

<p align="center">
<a href="https://github.com/fastack-dev/fastack"><img src="https://raw.githubusercontent.com/fastack-dev/fastack/main/docs/images/logo.png" alt="Fastack"></a>
</p>
<p align="center">
    <em>⚡ Fastack makes your FastAPI much easier 😎</em>
</p>
<p align="center">
<img alt="PyPI" src="https://img.shields.io/pypi/v/fastack?color=%23d3de37">
<img alt="PyPI - Status" src="https://img.shields.io/pypi/status/fastack">
<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/fastack?style=flat">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/fastack?style=flat">
<img alt="PyPI - License" src="https://img.shields.io/pypi/l/fastack?color=%2328a682">
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://results.pre-commit.ci/latest/github/fastack-dev/fastack/main"><img src="https://results.pre-commit.ci/badge/github/fastack-dev/fastack/main.svg"></a>
<a href="https://codecov.io/gh/fastack-dev/fastack">
<img src="https://codecov.io/gh/fastack-dev/fastack/branch/main/graph/badge.svg?token=01EBPHVTKX"/>
</a>
</p>

fastack is an intuitive framework based on FastAPI, for creating clean and easy-to-manage REST API project structures. It's built for FastAPI framework ❤️

## WARNING 🚨

This is an early development, lots of changes with each release. Also this is an experimental project, as I'm currently studying asynchronous environments.

FYI, this isn't the only intuitive framework project I've made. I've also made with different framework bases, including:

* [zemfrog](https://github.com/zemfrog/zemfrog) - Based on [Flask framework](https://flask.palletsprojects.com)
* [falca](https://github.com/aprilahijriyan/falca) - Based on [Falcon framework](https://falconframework.org/)



## Features 🔥

* Project layout (based on cookiecutter template)
* Pagination support
* Provide a `Controller` class for creating REST APIs
* Provides command line to manage app
* Support to access `app`, `request`, `state`, and `websocket` globally!
* and more!

## Plugins 🎉

List of official plugins:

* [fastack-sqlmodel](https://github.com/fastack-dev/fastack-sqlmodel) - [SQLModel](https://github.com/tiangolo/sqlmodel) integration for fastack.
* [fastack-migrate](https://github.com/fastack-dev/fastack-migrate) - [Alembic](https://alembic.sqlalchemy.org/en/latest/) integration for fastack.
* [fastack-mongoengine](https://github.com/fastack-dev/fastack-mongoengine) - [MongoEngine](https://github.com/MongoEngine/mongoengine) integration for fastack.
* [fastack-cache](https://github.com/fastack-dev/fastack-cache) - Caching plugin for fastack

## Installation 📦

```
pip install -U fastack
```

## Example 📚

Create a project

```
fastack new awesome-project
cd awesome-project
```

Install pipenv & create virtual environment

```
pip install pipenv && pipenv install && pipenv shell
```

Run app

```
fastack runserver
```

## Documentation 📖

For the latest documentation, see the [feature/docs](https://github.com/fastack-dev/fastack/tree/feature/docs) branch.

Build the latest documentation locally:

```
mkdocs serve
```

Or alternatively, you can visit https://fastack.readthedocs.io/en/latest/

## Tests 🔬

Run tests with ``tox``, maybe you need to install python version `3.7`, `3.8` and `3.9` first.

```
tox
```

All components have not been fully tested, feel free if anyone wants to help make unit tests :)
