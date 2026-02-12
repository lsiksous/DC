# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for v0.2.1
- [ ] Amélioration de l'UX
- [ ] Fonctionnalités supplémentaires à définir

## [0.1.1] - 2026-02-12

### Added
- Multi-showcase support (baseline + variants)
- Complete CV editing interface
- Skill level management (0-100%)
- Showcase selector in sidebar
- Create/delete variant functionality
- Export naming based on showcase name

### Changed
- Updated README to v0.1.1 with French documentation
- Cleaned up project structure
- Updated .gitignore patterns

### Removed
- `showcase.yaml` (moved to `showcases/baseline.yaml`)
- `convert_json_to_yaml.py` (replaced by `doyoubuzz_converter.py`)
- Objectives field from editor and converter
- Archive and cache directories

### Fixed
- DoYouBuzz JSON export format (results in separate array)
- Metadata preservation for round-trip compatibility

### Known Issues
- Results must be added manually in DoYouBuzz (JSON import limitation)

[Unreleased]: https://github.com/lsiksous/DC/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/lsiksous/DC/releases/tag/v0.1.1
