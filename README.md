# DoYouBuzz Showcase Editor

An interactive web application built with Streamlit to manage and edit professional showcase data with full **DoYouBuzz compatibility**.

## Features

- 📝 Edit personal information, summary, skills, experience (missions/context/environments), certifications, and languages
- 💾 Save changes to YAML format
- 📥 Export to DoYouBuzz-compatible JSON
- 📤 Import from DoYouBuzz JSON export
- 🔄 Full round-trip conversion (preserves DoYouBuzz IDs)
- 🎨 Clean, intuitive interface

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
- **missions**: List of tasks/responsibilities
- **context**: Project context/description  
- **environments**: Technical environment/stack

DoYouBuzz IDs are preserved with `_dyb_*` fields for round-trip compatibility.

## Deployment

This app can be deployed to Streamlit Community Cloud:
1. Push to GitHub
2. Connect your GitHub repository to Streamlit Cloud
3. Deploy!
