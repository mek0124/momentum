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
- Task model creation with proper default values
- ID validation method calls in controller
- Parameter handling in `update_task` method

### Changed
- Refactored to handle Task model conversion at core layer
- Improved error handling and validation

## [0.8.0] - yyyy-mm-dd
### Changed
- Updated `update_task` method to preserve existing task data
- Fixed method calls to match storage controller interface

## [0.6.0] - yyyy-mm-dd
### Added
- Task model with SQLAlchemy ORM mapping

### Changed
- Enhanced model structure for better database integration

## [0.4.0] - yyyy-mm-dd
### Added
- UUID generation for task IDs
- Created/updated timestamp management

## [0.2.0] - yyyy-mm-dd
### Added
- CoreController class for business logic
- Validators class with comprehensive input validation
- Initial model structure