# plinkliftover

<div align="center">

[![Build status](https://github.com/milescsmith/plinkliftover/workflows/build/badge.svg?branch=master&event=push)](https://github.com/milescsmith/plinkliftover/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/plinkliftover.svg)](https://pypi.org/project/plinkliftover/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/milescsmith/plinkliftover/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/milescsmith/plinkliftover/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/milescsmith/plinkliftover/releases)
[![License](https://img.shields.io/github/license/milescsmith/plinkliftover)](https://github.com/milescsmith/plinkliftover/blob/master/LICENSE)

Awesome `plinkliftover` is a Python cli/package created with https://github.com/TezRomacH/python-package-template

</div>

## Installation

```bash
pip install -U plinkliftover
```

or install with `Poetry`

```bash
poetry add plinkliftover
```

Then you can run

```bash
plinkliftover --help
```

```bash
plinkliftover --name Roman
```

or if installed with `Poetry`:

```bash
poetry run plinkliftover --help
```

```bash
poetry run plinkliftover --name Roman
```

## 📈 Releases

You can see the list of available releases on the [GitHub Releases](https://github.com/milescsmith/plinkliftover/releases) page.

We follow [Semantic Versions](https://semver.org/) specification.

We use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.

For Pull Request this labels are configured, by default:

|               **Label**               |  **Title in Releases**  |
| :-----------------------------------: | :---------------------: |
|       `enhancement`, `feature`        |       🚀 Features       |
| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |
|       `build`, `ci`, `testing`        | 📦 Build System & CI/CD |
|              `breaking`               |   💥 Breaking Changes   |
|            `documentation`            |    📝 Documentation     |
|            `dependencies`             | ⬆️ Dependencies updates |

You can update it in [`release-drafter.yml`](https://github.com/milescsmith/plinkliftover/blob/master/.github/release-drafter.yml).

GitHub creates the `bug`, `enhancement`, and `documentation` labels for you. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of your GitHub repository, when you need them.

## 🛡 License

[![License](https://img.shields.io/github/license/milescsmith/plinkliftover)](https://github.com/milescsmith/plinkliftover/blob/master/LICENSE)

This project is licensed under the terms of the `GNU GPL v3.0` license. See [LICENSE](https://github.com/milescsmith/plinkliftover/blob/master/LICENSE) for more details.

## 📃 Citation

```
@misc{plinkliftover,
  author = {Miles Smith <miles-smith@omrf.org>},
  title = {Awesome `plinkliftover` is a Python cli/package created with https://github.com/TezRomacH/python-package-template},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/milescsmith/plinkliftover}}
}
```

## Credits

This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template).
