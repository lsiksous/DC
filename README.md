# DoYouBuzz Showcase Editor

An interactive web application built with Streamlit to manage and edit professional showcase data with **PERFECT DoYouBuzz compatibility**.

## ✨ Perfect Bidirectional Sync

This editor provides **100% lossless round-trip conversion** between DoYouBuzz JSON and editable YAML format:
- ✅ All 37 top-level DoYouBuzz fields preserved
- ✅ All nested structures (skills, experiences, missions, etc.) preserved perfectly
- ✅ All metadata fields (IDs, timestamps, logos, etc.) preserved
- ✅ Guaranteed byte-for-byte identical export = original JSON

## Features

- 📝 Edit personal information, summary, experience (missions/context/environments), certifications, and languages
- 💾 Save changes to YAML format
- 📥 Export to DoYouBuzz-compatible JSON
- 📤 Import from DoYouBuzz JSON export
- 🔄 **PERFECT** round-trip conversion (100% metadata preservation)
- 🎨 Clean, intuitive interface
- 🛡️ Skills section preserved as-is (read-only, too complex for manual editing)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Running locally
```bash
streamlit run app.py
```

### Importing from DoYouBuzz

1. Export your CV from DoYouBuzz as JSON
2. Convert to editable YAML:
   ```bash
   python doyoubuzz_converter.py json2yaml your_cv.json showcase.yaml
   ```
3. Edit in the Streamlit app

### Exporting back to DoYouBuzz

1. Click "Export to DoYouBuzz JSON" in the sidebar
2. Download `showcase_export.json`
3. Import back to DoYouBuzz

## Structure

- `app.py` - Main Streamlit application
- `showcase.yaml` - Simplified YAML for editing
- `showcase.original.json` - Original DoYouBuzz JSON (for reference)
- `doyoubuzz_converter.py` - Bidirectional JSON<->YAML converter
- `requirements.txt` - Python dependencies

## Data Structure

The YAML uses a simplified structure for easy editing:
- **missions**: List of tasks/responsibilities with metadata
- **context**: Project context/description  
- **environments**: Technical environment/stack
- **results**: Achievement lists (empty arrays supported)
- **objectives**: Goal lists (empty arrays supported)

All DoYouBuzz metadata is automatically preserved:
- `_dyb_*` fields store IDs, sort orders, and other metadata
- `_doyoubuzz_metadata` section stores all top-level DoYouBuzz fields
- Full objects preserved for skills, certificates, languages, and experience metadata

This ensures **perfect round-trip compatibility** - your export will be byte-for-byte identical to the original JSON!

## Deployment

This app can be deployed to Streamlit Community Cloud:
1. Push to GitHub
2. Connect your GitHub repository to Streamlit Cloud
3. Deploy!
