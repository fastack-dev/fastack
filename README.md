# Fastack

fastack is an intuitive framework based on FastAPI, for creating clean and easy-to-manage REST API project structures. It's built for FastAPI framework ❤️

The goals of this project are:

* Create a clean and easy-to-manage REST API project structure
* Create a REST API with our ``Controller`` class
* Include pagination
* Support adding own commands using the ``typer`` library
* Plugin support
* Integrated with docker
* Integrated with pre-commit tool


## Plugins

List of official plugins:

* [fastack-sqlmodel](https://github.com/fastack-dev/fastack-sqlmodel) - [SQLModel](https://github.com/tiangolo/sqlmodel) integration for fastack.
* [fastack-migrate](https://github.com/fastack-dev/fastack-migrate) - [Alembic](https://alembic.sqlalchemy.org/en/latest/) integration for fastack.
* [fastack-mongoengine](https://github.com/fastack-dev/fastack-mongoengine) - [MongoEngine](https://github.com/MongoEngine/mongoengine) integration for fastack.
* [fastack-cache](https://github.com/fastack-dev/fastack-cache) - Caching plugin for fastack heart

## Installation

```
pip install fastack
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

Sorry in advance, for the documentation I haven't had time to make it 🙏
