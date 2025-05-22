# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.6.0] - 2025-05-27

### Fixed

- The `csv-table-no-translate` directive correctly renders the inner text of cross-references to other documents when using MyST-Parser for Markdown files

### Changed

- Dropped support for Python 3.8 and lower, as these are end of life
- Dropped support for myst-parser<0.18 as that uses an version of Sphinx so old it causes issues
- Only test on Linux, as standard for Open Data Services libraries

## [0.5.0] - 2022-09-26

### Changed

- Parse the text for the `jsoninclude-quote` directive as markdown

## [0.4.0] - 2022-09-02

### Added

- Add `jsoninclude-quote` directive

## [0.3.1] - 2022-08-03

- Fix markdown related directives to work with myst-parser 0.18.0

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

