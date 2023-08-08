# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adh
## [0.0.5] 2023-08-07

### Fixed
- Fix version specifier in pyproject.toml

## [0.0.4] 2023-08-07

### Changed
- Switched from 'ast.literal_eval' to 'json.loads' in JSONDirective

### Removed
- Remove trailing newline from JOSONDirective.instructions

## [0.0.3] 2023-08-06

### Added

- Add abstract `instructions` property to abstract base class `Directive`
- Add _info method to easily create info dict for directive
- Add tutorial for directives
- Add OpenAI wrapper to easily use OpenAI API with lobsang

### Changed

- Implement `embed` of `Directive` to use `instructions` as template to embed message and return dict with `directive`
  and `original` keys
- Implement `parse` of `Directive` to add `directive` and `**kwargs` to returned dict (still abstractmethod)

### Removed

- Remove `directive` and `query` in `chat._invoke_with_directive` since it is now handled by `Directive` class

## [0.0.2] 2023-08-04

Keeping this short, since no one is using this yet.

### Added

- Example for basic usage of the library

### Changed

- Rework the `Chat` class to be more simple and easy to use.

### Fixed

- Fix bugs in pyproject.toml and __init__.py

## [0.0.1] 2023-07-31

Initial Release

