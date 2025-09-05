# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.7.0] - 2025-09-09

### Added
- Added docstrings to all functions in `plinkliftover.liftover`

### Fix
- Overhauled `plinkliftover.liftover.lift_ped_loop`, including a pretty substantial bug fix

### Replace
- Swapped out `plinkliftover.logger` with a newer version from [scorphan](https://github.com/milescsmith/scorphan)

## [0.6.1] - 2025-09-05

### Fix
- replaced `distutils.find_executable` with `shutil.which` since `distutils` was removed in Python3.12

## [0.6.0] - 2025-07-16

### Change
- Update all dependencies so dependbot will stop screaming at me
  - Removed `better_exceptions` (it hasn't been updated in 3+ years) and `psutil` (wasn't being used)
- Switch to linting with ruff/ty
- Removed outdated dockerfile and github actions

## [0.5.2] - 2023-09-05

### Change

- Update dependancies and remove unnecessary development deps.


## [0.5.1] - 2023-07-18

### Change

- Remove ProgressParallel class. Replace all uses of this class with `joblib.Parallel`, passing "return_as=generator"
  to speed things up/reduce memory usage


## [0.5.0] - 2023-07-17

### Change

- Overhaul how the conversions and writing work so that they are now
  performed using a modified form of `joblib.Parallel`
  - Replaced all for loops with using the Parallel/delayed combo
- Replace `typer.progressbar` with `tqdm.rich` (because the latter works with the modified 
  `joblib.Parallel` class)

## [0.4.2] - 2023-07-17

### Fix

- Minimum python version
- running `plinkliftover` with no arguments now shows the help


## [0.4.1]

### Added

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

[0.7.0]: https://github.com/milescsmith/PLINKLiftOver/compare/0.6.1...0.7.0
[0.6.1]: https://github.com/milescsmith/PLINKLiftOver/compare/0.6.0...0.6.1
[0.6.0]: https://github.com/milescsmith/PLINKLiftOver/compare/0.5.2...0.6.0
[0.5.2]: https://github.com/milescsmith/PLINKLiftOver/compare/0.5.1...0.5.2
[0.5.1]: https://github.com/milescsmith/PLINKLiftOver/compare/0.5.0...0.5.1
[0.5.0]: https://github.com/milescsmith/PLINKLiftOver/compare/0.4.2...0.5.0
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
