# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - yyyy-mm-dd
### Added
### Changed
### Fixed

## [1.0.0] - 2025-12-03
### Fixed
- Parameter handling in `add_task` command
- ID validation in all commands requiring task IDs

### Changed
- Updated from version 0.8.0 to 1.0.0
- Refactored command structure for consistency
- Improved error messages and user experience

## [0.8.0] - yyyy-mm-dd
### Added
- Integration with tm_config for storage preferences
- Proper error handling with user-friendly messages

### Changed
- Refactored command structure for better organization
- Updated validation flow

## [0.6.0] - yyyy-mm-dd
### Added
- `edit_task`: Update existing tasks with partial updates
- `delete_task`: Remove tasks by ID
- `list_tasks`: List all tasks or specific task by ID

## [0.4.0] - yyyy-mm-dd
### Added
- `add_task`: Create new tasks with validation
- Command validation using tm_core validators

## [0.2.0] - yyyy-mm-dd
### Added
- Initial CLI interface structure
- Basic command framework using Click
- Project setup and configuration