# Task Manager Changelog

## v1.0.0 - 2025-12-03
- **CLI**: Fixed parameter handling and ID validation; refactored command structure for consistency
- **Config**: Fixed UTF-8 encoding and type hints; version stabilized to 1.0.0
- **Core**: Fixed task model creation and validation; improved error handling
- **Storage**: Fixed method name consistency and database operations

## v0.8.0 - yyyy-mm-dd
- **CLI**: Integrated with config for storage preferences; improved error handling
- **Config**: Fixed JSON parsing; improved configuration management
- **Core**: Updated update_task method; fixed storage controller interface calls
- **Storage**: Updated to accept Task models; improved error handling

## v0.6.0 - yyyy-mm-dd
- **CLI**: Added edit, delete, and list task commands
- **Config**: Added automatic config file creation; refactored loading mechanism
- **Core**: Added SQLAlchemy Task model; enhanced model structure
- **Storage**: Added Database class with SQLAlchemy; fixed session management

## v0.4.0 - yyyy-mm-dd
- **CLI**: Added add_task command with core validation
- **Config**: Added version and database configuration management
- **Core**: Added UUID generation and timestamp management
- **Storage**: Reconstructed to be 'local storage first'; added get_db_path

## v0.2.0 - yyyy-mm-dd
- **CLI**: Initial CLI interface structure with Click framework
- **Config**: Initial Config class with JSON-based configuration
- **Core**: Added CoreController and Validators with initial model structure
- **Storage**: Added StorageController with offline/online support and fallback

## [Unreleased]
- Changes to be documented in future releases