# Contributing

Thank you in advance for taking the time to contribute to this project 🙏


## Report an issue

You can track or report issues to this project via the following link:

https://github.com/fastack-dev/fastack/issues 🚀

Before reporting an issue, make sure you've looked for a similar issue. So there will be no duplication of issues 🤧

## Code

The first step you must do before contributing.

### Clone source code

```
git clone https://github.com/fastack-dev/fastack.git
cd fastack
```

### Install poetry

Fastack uses poetry as a package manager, so you will need to install it first, see here https://python-poetry.org/docs/#installation for installation details.

```
poetry install
poetry shell
```

If you use ``VSCode`` as a text editor, you have to set up your ``VSCode`` python interpreter according to the virtual environment created by ``poetry``

```
$ poetry env info -p
/home/mamang/.cache/pypoetry/virtualenvs/fastack-g40dxRvq-py3.8
```

If you execute the above command, the result that appears is the location of the virtual environment created by ``poetry``. So you need to add ``bin/python`` to the back of the virtual environment path.

Example:

```
/home/mamang/.cache/pypoetry/virtualenvs/fastack-g40dxRvq-py3.8/bin/python
```

And set python interpreter in ``VSCode``
See here https://code.visualstudio.com/docs/python/environments#_select-and-activate-an-environment for changing python interpreter in VSCode

### Configure pre-commit hooks

You need to configure fastack repository with pre-commit hook, this is needed for automatic code formatting when you push to remote repository.

```
pre-commit install
```

### Configure Git Flow

It is optional to use ``git-flow`` for efficient branching (for added features, bugfixes, etc).

For installation, you can see here https://danielkummer.github.io/git-flow-cheatsheet/index.html#setup

When you have finished installing ``git-flow``, initialize your repository with ``git-flow``:

```
$ git flow init
Which branch should be used for bringing forth production releases?
   - main
Branch name for production releases: [main]
Branch name for "next release" development: [develop] next

How to name your supporting branch prefixes?
Feature branches? [feature/]
Bugfix branches? [bugfix/]
Release branches? [release/]
Hotfix branches? [hotfix/]
Support branches? [support/]
Version tag prefix? [] v
Hooks and filters directory? [...]
```

For development branch set to ``next`` for next release (optional)


### Add features, bug fixes, etc.

Always creating new branches for feature additions, bug fixes, etc.

In this case I use ``git-flow``:

```
# Add features
git flow feature start awesome-feature
```

After adding features, commit the changes that have been made. Then publish to your repository.

!!! note

    You will also need to update documentation and unit testing.

```
git flow feature publish
```

Create pull request

!!! warning

    Before make a pull request, make sure it's synced with the main fastack repository.
