# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

** [0.4.2] - 2023-07-17

*** Fix

- Minimum python version
- running `plinkliftover` with no arguments now shows the help


** [0.4.1]

*** Added

- Updated gitignore


## [0.4.0] - 2023-07-13

### Change

- Update dependencies
- Adjust functions to use updated `typer` syntax
- Increase required python version to 3.10
- Switch from using `poetry` to `hatchling`/`huak`


## [0.3.0] - 2022-02-17

### Added

- Added cli interface for map2bed and bed2map

### Changed

- Split off `map2bed` and `bed2map` into separate submodules

## [0.2.0] - 2022-02-02

### Added

- A real README.md

### Changed

- Removed conditional requirement of `import_metadata` as a version of Python >=3.8 is required

## [0.1.11] - 2022-02-02

### Changed

- updated dependency versions

## [0.1.10] - 2021-12-20

### Changed

- updated dependency versions


## [0.1.9] - 2021-04-20

### Changed

- updated dependency versions

## [0.1.8] - 2021

### Changed

- renamed `logging.py` to `logger.py` to avoid colliding with the standard module name
- alter how the PED file is written to: for whatever reason, `Path().write_text()` was not working
  but using a open file context manager with `writelines()` does.
- make sure we bail out prematurely if there is a mismatch between the PED file and MAP file

## [0.1.7] - 2021-02-22

### Added

- CHANGELOG.md
- more logging info

### Fixed

- add missing import of liftPed to plinkliftover.__main__ from plinkliftover.liftover
- if the liftOver executable cannot be found, raise an error

## [0.1.6] - 2021-02-22

### Fixed

- replace `set` and `tuple` in type hints with their `typing.Set` and `typing.Tuple` counterparts

[0.4.2]: https://github.com/milescsmith/PLINKLiftOver/compare/0.4.1...0.4.2
[0.4.1]: https://github.com/milescsmith/PLINKLiftOver/compare/0.4.0...0.4.1
[0.4.0]: https://github.com/milescsmith/PLINKLiftOver/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/milescsmith/PLINKLiftOver/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/milescsmith/PLINKLiftOver/compare/0.1.11...0.2.0
[0.1.11]: https://github.com/milescsmith/PLINKLiftOver/compare/0.1.10...0.1.11
[0.1.10]: https://github.com/milescsmith/PLINKLiftOver/compare/0.1.9...0.1.10
[0.1.9]: https://github.com/milescsmith/PLINKLiftOver/compare/0.1.8...0.1.9
[0.1.8]: https://github.com/milescsmith/PLINKLiftOver/compare/0.1.7...0.1.8
[0.1.7]: https://github.com/milescsmith/PLINKLiftOver/compare/0.1.6...0.1.7
[0.1.6]: https://github.com/milescsmith/PLINKLiftOver/compare/0.1.6...0.1.6
[0.1.5]: https://github.com/milescsmith/PLINKLiftOver/releases/tag/0.1.5
