# Release v0.1.1 - DoYouBuzz Showcase Editor

**Date**: 2026-02-12  
**Tag**: `v0.1.1`

## 🎯 Overview

First stable release of the DoYouBuzz Showcase Editor - a Streamlit web application for managing and editing professional CV data with multi-showcase support.

## ✨ Features

### Multi-Showcase Management
- 📌 **Baseline showcase**: Main CV tracked in Git
- 📄 **Variant creation**: Create specialized versions (frontend, backend, data engineer, etc.)
- 🔄 **Easy switching**: Toggle between showcases in the sidebar
- ♻️ **Duplication**: Create variants from any existing showcase

### Complete CV Editing
- 👤 **Personal Information**: Name, title, email, location
- 📝 **Professional Summary**: Editable description
- 🛠️ **Skills**: Category-based management with levels (0-100%)
- 💼 **Professional Experience**:
  - Job title, company, dates, location
  - Detailed context
  - Missions (tasks performed)
  - Results (achievements)
  - Technical environment
- 🎓 **Certifications**: Name, issuing organization, date
- 🌍 **Languages**: Language and proficiency level

### Import/Export
- 📥 Import JSON from DoYouBuzz
- 📤 Export JSON to DoYouBuzz
- 💾 Automatic YAML save
- 🔄 Metadata preservation for round-trip compatibility

## 🔧 Technical Improvements

- **Project cleanup**: Reduced to 788 KB (removed old files and archives)
- **Removed objectives field**: Not supported by DoYouBuzz JSON import
- **Updated .gitignore**: Excludes exports and temporary files
- **Comprehensive README**: Complete usage guide in French

## ⚠️ Known Limitations

DoYouBuzz JSON import does **NOT** support:
- ❌ **Results**: Must be added manually in DoYouBuzz interface
- ❌ **Objectives**: Removed from editor (not used)

**Workaround**: Use the provided Python script to list results for easy copy-paste into DoYouBuzz.

## 📦 Installation

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🔗 Links

- **Repository**: https://github.com/lsiksous/DC
- **Commit**: `a39d508`

## 📝 Changelog

### Added
- Multi-showcase support with baseline and variants
- Complete CV editing interface with all sections
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

## 🙏 Credits

Co-Authored-By: Warp <agent@warp.dev>

---

**Full Changelog**: https://github.com/lsiksous/DC/commits/v0.1.1
