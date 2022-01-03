# Fastack

fastack is an intuitive framework based on FastAPI, for creating clean and easy-to-manage REST API project structures. It's built for FastAPI framework ❤️

## Features

* Project layout (based on cookiecutter template)
* Pagination support
* Provide a `Controller` class for creating REST APIs
* Provides command line to manage app

## Plugins

List of official plugins:

* [fastack-sqlmodel](https://github.com/fastack-dev/fastack-sqlmodel) - [SQLModel](https://github.com/tiangolo/sqlmodel) integration for fastack.
* [fastack-migrate](https://github.com/fastack-dev/fastack-migrate) - [Alembic](https://alembic.sqlalchemy.org/en/latest/) integration for fastack.
* [fastack-mongoengine](https://github.com/fastack-dev/fastack-mongoengine) - [MongoEngine](https://github.com/MongoEngine/mongoengine) integration for fastack.
* [fastack-cache](https://github.com/fastack-dev/fastack-cache) - Caching plugin for fastack

## Installation

```
pip install -U fastack
```

## Example

create project structure

```
fastack new awesome-project
cd awesome-project
```

install pipenv & create virtual environment

```
pip install pipenv && pipenv install && pipenv shell
```

run app

```
fastack runserver
```

## Documentation

For the latest documentation, see the [feature/docs](https://github.com/fastack-dev/fastack/tree/feature/docs) branch.
