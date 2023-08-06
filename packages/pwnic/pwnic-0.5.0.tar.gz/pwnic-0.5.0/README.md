# pwnic

<div align="center">

[![Build status](https://github.com/parmigggiana/pwnic/workflows/build/badge.svg?branch=master&event=push)](https://github.com/parmigggiana/pwnic/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/pwnic.svg)](https://pypi.org/project/pwnic/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![License](https://img.shields.io/github/license/parmigggiana/pwnic)](https://github.com/parmigggiana/pwnic/blob/master/LICENSE)
![Coverage Report](assets/images/coverage.svg)


</div>

## What is this?
`pwnic` is a python package built to forget about the boring stuff during your A/D CTF. 
It will take care of both attacking and submitting. 
It's only interface is a RESTful API built with FastAPI providing every functionality you need. 
You can use our beautiful frontend (WIP) or build your own. 
Check out /docs to reference the API.

## Install

## Usage

## 📈 Releases

You can see the list of available releases on the [GitHub Releases](https://github.com/pwnic/pwnic/releases) page.

We follow [Semantic Versions](https://semver.org/) specification.

We use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.

### List of labels and corresponding titles

|               **Label**               |  **Title in Releases**  |
| :-----------------------------------: | :---------------------: |
|       `enhancement`, `feature`        |       🚀 Features       |
| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |
|       `build`, `ci`, `testing`        | 📦 Build System & CI/CD |
|              `breaking`               |   💥 Breaking Changes   |
|            `documentation`            |    📝 Documentation     |
|            `dependencies`             | ⬆️ Dependencies updates |

You can update it in [`release-drafter.yml`](https://github.com/pwnic/pwnic/blob/master/.github/release-drafter.yml).

GitHub creates the `bug`, `enhancement`, and `documentation` labels for you. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of your GitHub repository, when you need them.

## 🛡 License

[![License](https://img.shields.io/github/license/pwnic/pwnic)](https://github.com/pwnic/pwnic/blob/master/LICENSE)

This project is licensed under the terms of the `GNU GPL v3.0` license. See [LICENSE](https://github.com/pwnic/pwnic/blob/master/LICENSE) for more details.

## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)

This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)
