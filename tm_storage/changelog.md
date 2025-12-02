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
- Method name consistency (`list_task_by_id` vs `get_task_by_id`)
- Task model handling in update operations
- Database path and directory creation

## [0.8.0] - yyyy-mm-dd
### Changed
- Updated to accept Task models instead of dictionaries
- Consistent method signatures across controllers
- Improved error handling in database operations

## [0.6.0] - yyyy-mm-dd
### Added
- Database class with SQLAlchemy integration
- Automatic database initialization and table creation

### Fixed
- Session management for database operations
- Data model to dictionary conversion

## [0.4.0] - yyyy-mm-dd
### Changed
- Reconstructed controller.py and controllers/offline.py to be 'local storage first' in storage.
- Created `get_db_path` instead of creating the path in every function.

### Fixed
- If online connection fails, default storage is relational
- Fixed return types

## [0.2.0] - yyyy-mm-dd
### Added
- StorageController for abstracting storage operations
- OfflineStorageController for SQLite database operations
- OnlineStorageController interface (not implemented)

### Fixed
- Support for both online and offline storage modes
- Connection fallback from online to offline storage
- Basic wrapper functions for storage operations