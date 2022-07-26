# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2022-07-26

### Added

- Add myst-parser 0.18.0 support

## [0.2.0] - 2021-07-07

### Removed

- Remove dependency on recommonmark, and remove AutoStructifyLowPriority class. Please use myst-parser instead. https://github.com/readthedocs/recommonmark/issues/221

## [0.1.1] - 2021-05-18

### Fixed

- Fix the markdown directive, so it doesn't fail on anything that required sphinx (and not just docutils) formatting.

## [0.1.0] - 2021-05-11

First release of project (was previously included by pip installing from a git commit).

