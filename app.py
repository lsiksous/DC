import streamlit as st
import yaml
import json
from pathlib import Path
from datetime import datetime
import showcase_manager as sm

# Page config
st.set_page_config(
    page_title="DoYouBuzz Showcase Editor",
    page_icon="📄",
    layout="wide"
)

# Initialize current showcase in session state
if 'current_showcase' not in st.session_state:
    showcases = sm.list_showcases()
    st.session_state.current_showcase = showcases[0] if showcases else 'baseline'

# Dynamic file paths based on current showcase
YAML_FILE = sm.get_showcase_path(st.session_state.current_showcase)
JSON_EXPORT = Path("showcase.json")

# Load data
def load_yaml(file_path):
    """Load YAML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        st.error(f"Error loading YAML: {e}")
        return None

def save_yaml(data, file_path):
    """Save data to YAML file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=float('inf'))
        return True
    except Exception as e:
        st.error(f"Error saving YAML: {e}")
        return False

def export_json(data, file_path):
    """Export data to JSON file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Error exporting JSON: {e}")
        return False

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = sm.load_showcase(st.session_state.current_showcase)

# Header
st.title(f"📄 DoYouBuzz Showcase Editor")
st.caption(f"Editing: **{st.session_state.current_showcase}** {'(Baseline)' if st.session_state.current_showcase == 'baseline' else '(Variant)'}")
st.markdown("---")

# Sidebar for navigation and actions
with st.sidebar:
    # Showcase selector
    st.header("🎯 Showcase")
    showcases = sm.list_showcases()
    
    if showcases:
        current_idx = showcases.index(st.session_state.current_showcase) if st.session_state.current_showcase in showcases else 0
        selected = st.selectbox(
            "Select showcase:",
            showcases,
            index=current_idx,
            format_func=lambda x: f"📌 {x}" if x == 'baseline' else f"📄 {x}"
        )
        
        if selected != st.session_state.current_showcase:
            st.session_state.current_showcase = selected
            st.session_state.data = sm.load_showcase(selected)
            st.rerun()
    
    # Create variant button
    with st.expander("➕ Create Variant"):
        variant_name = st.text_input("Variant name (e.g., 'frontend', 'backend')")
        variant_desc = st.text_input("Description (optional)")
        if st.button("Create") and variant_name:
            if sm.create_variant(st.session_state.current_showcase, variant_name, variant_desc):
                st.success(f"✅ Created variant: {variant_name}")
                st.session_state.current_showcase = variant_name
                st.rerun()
            else:
                st.error("❌ Failed to create variant (may already exist)")
    
    # Delete button (only for variants)
    if st.session_state.current_showcase != 'baseline':
        if st.button("🗑️ Delete This Showcase", type="secondary"):
            if st.checkbox("Confirm delete"):
                if sm.delete_showcase(st.session_state.current_showcase):
                    st.success("Deleted!")
                    st.session_state.current_showcase = 'baseline'
                    st.rerun()
    
    st.markdown("---")
    st.header("Navigation")
    section = st.radio(
        "Choose section to edit:",
        ["Personal Info", "Summary", "Skills", "Experience", "Certifications", "Languages", "Export/Import"]
    )
    
    st.markdown("---")
    st.header("Actions")
    
    if st.button("💾 Save to YAML", type="primary"):
        if sm.save_showcase(st.session_state.current_showcase, st.session_state.data):
            st.success(f"✅ Saved {st.session_state.current_showcase} successfully!")
            st.info(f"File size: {YAML_FILE.stat().st_size} bytes")
        else:
            st.error("❌ Save failed!")
    
    if st.button("📥 Export to DoYouBuzz JSON"):
        # Use doyoubuzz_converter for proper format
        import subprocess
        yaml_path = str(sm.get_showcase_path(st.session_state.current_showcase))
        export_name = f"{st.session_state.current_showcase}_export.json"
        original_json = str(sm.get_showcase_path(st.session_state.current_showcase).with_suffix('.original.json'))
        
        result = subprocess.run([
            'python', 'doyoubuzz_converter.py', 'yaml2json',
            yaml_path, export_name, original_json
        ], capture_output=True, text=True)
        if result.returncode == 0:
            st.success(f"✅ Exported to {export_name} (DoYouBuzz compatible)")
        else:
            st.error(f"Export failed: {result.stderr}")
    
    if st.button("🔄 Reload from file"):
        # Force reload by clearing any cache
        st.session_state.data = sm.load_showcase(st.session_state.current_showcase)
        st.success("✅ Reloaded from file!")
        st.rerun()

# Main content area
if st.session_state.data is None:
    st.error("Failed to load data. Please check the YAML file.")
else:
    data = st.session_state.data
    
    # Personal Info Section
    if section == "Personal Info":
        st.header("👤 Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            data['personal_info']['name'] = st.text_input("Name", data['personal_info'].get('name', ''))
            data['personal_info']['email'] = st.text_input("Email", data['personal_info'].get('email', ''))
            data['personal_info']['phone'] = st.text_input("Phone", data['personal_info'].get('phone', ''))
            data['personal_info']['location'] = st.text_input("Location", data['personal_info'].get('location', ''))
        
        with col2:
            data['personal_info']['title'] = st.text_input("Professional Title", data['personal_info'].get('title', ''))
            data['personal_info']['website'] = st.text_input("Website", data['personal_info'].get('website', ''))
            data['personal_info']['linkedin'] = st.text_input("LinkedIn", data['personal_info'].get('linkedin', ''))
            data['personal_info']['github'] = st.text_input("GitHub", data['personal_info'].get('github', ''))
    
    # Summary Section
    elif section == "Summary":
        st.header("📝 Professional Summary")
        data['summary'] = st.text_area("Summary", data.get('summary', ''), height=300)
    
    # Skills Section
    elif section == "Skills":
        st.header("🛠️ Skills")
        
        if 'skills' not in data or data['skills'] is None:
            data['skills'] = []
        
        # Add new skill category
        with st.expander("➕ Add New Skill Category"):
            new_category = st.text_input("Category name")
            if st.button("Add Category") and new_category:
                data['skills'].append({'category': new_category, 'items': []})
                st.success(f"Added category: {new_category}")
                st.rerun()
        
        # Edit existing skills
        for idx, skill_cat in enumerate(data['skills']):
            with st.expander(f"📦 {skill_cat['category']}", expanded=False):
                skill_cat['category'] = st.text_input(f"Category name", skill_cat['category'], key=f"cat_{idx}")
                
                # Items
                st.markdown("**Skills in this category:**")
                items = skill_cat.get('items', [])
                
                # Edit existing items
                for item_idx, item in enumerate(items):
                    # Handle both new dict format and old string format
                    if isinstance(item, dict):
                        skill_name = item.get('name', '')
                        skill_level = item.get('level', 0)
                    else:
                        # Old string format: "Skill (80%)" or just "Skill"
                        item_str = str(item)
                        if '(' in item_str and ')' in item_str:
                            skill_name = item_str.split('(')[0].strip()
                            level_str = item_str.split('(')[1].split(')')[0].replace('%', '').strip()
                            skill_level = int(level_str) if level_str.isdigit() else 0
                        else:
                            skill_name = item_str
                            skill_level = 0
                    
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        new_name = st.text_input(f"Skill {item_idx + 1}", skill_name, key=f"skill_{idx}_{item_idx}", label_visibility="collapsed")
                    with col2:
                        new_level = st.number_input("Level %", value=skill_level, min_value=0, max_value=100, step=5, key=f"level_{idx}_{item_idx}", label_visibility="collapsed")
                    with col3:
                        if st.button("🗑️", key=f"del_{idx}_{item_idx}"):
                            skill_cat['items'].pop(item_idx)
                            st.rerun()
                    
                    # Update the item with new values, preserving metadata
                    if isinstance(item, dict):
                        skill_cat['items'][item_idx]['name'] = new_name
                        skill_cat['items'][item_idx]['level'] = new_level
                    else:
                        # Convert old format to new format
                        skill_cat['items'][item_idx] = {'name': new_name, 'level': new_level}
                
                # Add new item
                st.markdown("**Add new skill:**")
                col1, col2 = st.columns([3, 1])
                with col1:
                    new_item_name = st.text_input("Skill name", key=f"new_skill_name_{idx}")
                with col2:
                    new_item_level = st.number_input("Level %", value=0, min_value=0, max_value=100, step=5, key=f"new_skill_level_{idx}")
                
                if st.button("Add Skill", key=f"add_skill_{idx}") and new_item_name:
                    skill_cat['items'].append({'name': new_item_name, 'level': new_item_level})
                    st.rerun()
                
                # Delete category
                if st.button("🗑️ Delete Category", key=f"del_cat_{idx}"):
                    data['skills'].pop(idx)
                    st.rerun()
    
    # Experience Section
    elif section == "Experience":
        st.header("💼 Professional Experience")
        
        if 'experience' not in data or data['experience'] is None:
            data['experience'] = []
        
        # Add new experience
        with st.expander("➕ Add New Experience"):
            new_exp = {
                'title': st.text_input("Job Title"),
                'company': st.text_input("Company"),
                'location': st.text_input("Location"),
                'start_date': st.text_input("Start Date (e.g., 2024-01)"),
                'end_date': st.text_input("End Date (e.g., 2024-12 or 'Present')"),
                'context': st.text_area("Context / Description", height=150),
                'missions': [],
                'results': [],
                'objectives': [],
                'environments': []
            }
            
            if st.button("Add Experience") and new_exp['title'] and new_exp['company']:
                data['experience'].insert(0, new_exp)
                st.success("Added new experience!")
                st.rerun()
        
        # Edit existing experiences
        for idx, exp in enumerate(data['experience']):
            with st.expander(f"🏢 {exp.get('title', 'Untitled')} @ {exp.get('company', 'Unknown')}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    exp['title'] = st.text_input("Job Title", exp.get('title', ''), key=f"exp_title_{idx}")
                    exp['company'] = st.text_input("Company", exp.get('company', ''), key=f"exp_company_{idx}")
                    exp['location'] = st.text_input("Location", exp.get('location', ''), key=f"exp_location_{idx}")
                
                with col2:
                    exp['start_date'] = st.text_input("Start Date", exp.get('start_date', ''), key=f"exp_start_{idx}")
                    exp['end_date'] = st.text_input("End Date", exp.get('end_date', ''), key=f"exp_end_{idx}")
                
                exp['context'] = st.text_area("Context / Description", exp.get('context', exp.get('description', '')), key=f"exp_ctx_{idx}", height=150)
                
                # Missions
                st.markdown("**Missions:**")
                missions = exp.get('missions', exp.get('achievements', []))
                if not isinstance(missions, list):
                    missions = []
                new_missions = []
                
                for mis_idx, mission in enumerate(missions):
                    # Handle both dict (with _dyb_id) and string formats
                    if isinstance(mission, dict):
                        mission_text = mission.get('description', '')
                        mission_meta = {'_dyb_id': mission.get('_dyb_id'), '_dyb_sort': mission.get('_dyb_sort', mis_idx)}
                    else:
                        mission_text = str(mission)
                        mission_meta = {}
                    
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        new_mis = st.text_area(f"Mission {mis_idx + 1}", mission_text, key=f"mis_{idx}_{mis_idx}", height=120, label_visibility="collapsed")
                        if new_mis:
                            # Preserve metadata if it exists
                            if mission_meta.get('_dyb_id'):
                                new_missions.append({'description': new_mis, **mission_meta})
                            else:
                                new_missions.append(new_mis)
                    with col2:
                        st.markdown("<br>", unsafe_allow_html=True)  # Align delete button
                        if st.button("🗑️", key=f"del_mis_{idx}_{mis_idx}"):
                            exp['missions'].pop(mis_idx)
                            st.rerun()
                
                exp['missions'] = new_missions
                
                # Add new mission
                new_mis_input = st.text_area("Add new mission", key=f"new_mis_{idx}", height=120)
                if st.button("Add Mission", key=f"add_mis_{idx}") and new_mis_input:
                    exp['missions'].append(new_mis_input)
                    st.rerun()
                
                # Results
                st.markdown("**Results:**")
                results = exp.get('results', [])
                if not isinstance(results, list):
                    results = []
                new_results = []
                
                for res_idx, result in enumerate(results):
                    # Handle both dict (with _dyb_id) and string formats
                    if isinstance(result, dict):
                        result_text = result.get('description', '')
                        result_meta = {'_dyb_id': result.get('_dyb_id'), '_dyb_sort': result.get('_dyb_sort', res_idx)}
                    else:
                        result_text = str(result)
                        result_meta = {}
                    
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        new_res = st.text_area(f"Result {res_idx + 1}", result_text, key=f"res_{idx}_{res_idx}", height=100, label_visibility="collapsed")
                        if new_res:
                            # Preserve metadata if it exists
                            if result_meta.get('_dyb_id'):
                                new_results.append({'description': new_res, **result_meta})
                            else:
                                new_results.append(new_res)
                    with col2:
                        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
                        if st.button("🗑️", key=f"del_res_{idx}_{res_idx}"):
                            exp['results'].pop(res_idx)
                            st.rerun()
                
                exp['results'] = new_results
                
                # Add new result
                new_res_input = st.text_area("Add new result", key=f"new_res_{idx}", height=100)
                if st.button("Add Result", key=f"add_res_{idx}") and new_res_input:
                    exp['results'].append(new_res_input)
                    st.rerun()
                
                # Objectives
                st.markdown("**Objectives:**")
                objectives = exp.get('objectives', [])
                if not isinstance(objectives, list):
                    objectives = []
                new_objectives = []
                
                for obj_idx, objective in enumerate(objectives):
                    # Handle both dict (with _dyb_id) and string formats
                    if isinstance(objective, dict):
                        obj_text = objective.get('description', '')
                        obj_meta = {'_dyb_id': objective.get('_dyb_id'), '_dyb_sort': objective.get('_dyb_sort', obj_idx)}
                    else:
                        obj_text = str(objective)
                        obj_meta = {}
                    
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        new_obj = st.text_area(f"Objective {obj_idx + 1}", obj_text, key=f"obj_{idx}_{obj_idx}", height=100, label_visibility="collapsed")
                        if new_obj:
                            # Preserve metadata if it exists
                            if obj_meta.get('_dyb_id'):
                                new_objectives.append({'description': new_obj, **obj_meta})
                            else:
                                new_objectives.append(new_obj)
                    with col2:
                        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
                        if st.button("🗑️", key=f"del_obj_{idx}_{obj_idx}"):
                            exp['objectives'].pop(obj_idx)
                            st.rerun()
                
                exp['objectives'] = new_objectives
                
                # Add new objective
                new_obj_input = st.text_area("Add new objective", key=f"new_obj_{idx}", height=100)
                if st.button("Add Objective", key=f"add_obj_{idx}") and new_obj_input:
                    exp['objectives'].append(new_obj_input)
                    st.rerun()
                
                # Environments
                st.markdown("**Technical Environments:**")
                environments = exp.get('environments', [])
                if not isinstance(environments, list):
                    environments = []
                new_envs = []
                
                for env_idx, environment in enumerate(environments):
                    # Handle both dict (with _dyb_id) and string formats
                    if isinstance(environment, dict):
                        env_text = environment.get('description', '')
                        env_meta = {'_dyb_id': environment.get('_dyb_id'), '_dyb_sort': environment.get('_dyb_sort', env_idx)}
                    else:
                        env_text = str(environment)
                        env_meta = {}
                    
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        new_env = st.text_area(f"Environment {env_idx + 1}", env_text, key=f"env_{idx}_{env_idx}", height=100, label_visibility="collapsed")
                        if new_env:
                            # Preserve metadata if it exists
                            if env_meta.get('_dyb_id'):
                                new_envs.append({'description': new_env, **env_meta})
                            else:
                                new_envs.append(new_env)
                    with col2:
                        if st.button("🗑️", key=f"del_env_{idx}_{env_idx}"):
                            exp['environments'].pop(env_idx)
                            st.rerun()
                
                exp['environments'] = new_envs
                
                # Add new environment
                new_env_input = st.text_area("Add new environment", key=f"new_env_{idx}", height=100)
                if st.button("Add Environment", key=f"add_env_{idx}") and new_env_input:
                    exp['environments'].append(new_env_input)
                    st.rerun()
                
                # Clean up old fields for backward compatibility
                if 'achievements' in exp and 'missions' not in exp:
                    exp['missions'] = exp.pop('achievements')
                if 'description' in exp and 'context' not in exp:
                    exp['context'] = exp.pop('description')
                
                # Delete experience
                if st.button("🗑️ Delete Experience", key=f"del_exp_{idx}"):
                    data['experience'].pop(idx)
                    st.rerun()
    
    # Certifications Section
    elif section == "Certifications":
        st.header("🎓 Certifications")
        
        if 'certifications' not in data or data['certifications'] is None:
            data['certifications'] = []
        
        # Add new certification
        with st.expander("➕ Add New Certification"):
            col1, col2 = st.columns(2)
            with col1:
                new_cert_name = st.text_input("Certification Name")
                new_cert_issuer = st.text_input("Issuer")
            with col2:
                new_cert_date = st.text_input("Date Obtained")
                new_cert_url = st.text_input("Credential URL")
            
            if st.button("Add Certification") and new_cert_name:
                data['certifications'].insert(0, {
                    'name': new_cert_name,
                    'issuer': new_cert_issuer,
                    'date': new_cert_date,
                    'credential_url': new_cert_url
                })
                st.success("Added new certification!")
                st.rerun()
        
        # Edit existing certifications
        for idx, cert in enumerate(data['certifications']):
            with st.expander(f"🏆 {cert.get('name', 'Untitled')}"):
                col1, col2 = st.columns(2)
                with col1:
                    cert['name'] = st.text_input("Name", cert.get('name', ''), key=f"cert_name_{idx}")
                    cert['issuer'] = st.text_input("Issuer", cert.get('issuer', ''), key=f"cert_issuer_{idx}")
                with col2:
                    cert['date'] = st.text_input("Date", cert.get('date', ''), key=f"cert_date_{idx}")
                    cert['credential_url'] = st.text_input("URL", cert.get('credential_url', ''), key=f"cert_url_{idx}")
                
                if st.button("🗑️ Delete Certification", key=f"del_cert_{idx}"):
                    data['certifications'].pop(idx)
                    st.rerun()
    
    # Languages Section
    elif section == "Languages":
        st.header("🌐 Languages")
        
        if 'languages' not in data or data['languages'] is None:
            data['languages'] = []
        
        # Add new language
        with st.expander("➕ Add New Language"):
            col1, col2 = st.columns(2)
            with col1:
                new_lang = st.text_input("Language")
            with col2:
                new_prof = st.text_input("Proficiency Level")
            
            if st.button("Add Language") and new_lang:
                data['languages'].append({'language': new_lang, 'proficiency': new_prof})
                st.success("Added new language!")
                st.rerun()
        
        # Edit existing languages
        for idx, lang in enumerate(data['languages']):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                lang['language'] = st.text_input("Language", lang.get('language', ''), key=f"lang_{idx}")
            with col2:
                lang['proficiency'] = st.text_input("Proficiency", lang.get('proficiency', ''), key=f"prof_{idx}")
            with col3:
                if st.button("🗑️", key=f"del_lang_{idx}"):
                    data['languages'].pop(idx)
                    st.rerun()
    
    # Export/Import Section
    elif section == "Export/Import":
        st.header("📤 Export / Import")
        
        tab1, tab2 = st.tabs(["Export", "Import"])
        
        with tab1:
            st.subheader("Export your data")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**YAML Format**")
                yaml_str = yaml.dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False)
                st.download_button(
                    label="📥 Download YAML",
                    data=yaml_str,
                    file_name=f"showcase_{datetime.now().strftime('%Y%m%d')}.yaml",
                    mime="text/yaml"
                )
                with st.expander("Preview YAML"):
                    st.code(yaml_str, language='yaml')
            
            with col2:
                st.markdown("**JSON Format**")
                json_str = json.dumps(data, ensure_ascii=False, indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_str,
                    file_name=f"showcase_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
                with st.expander("Preview JSON"):
                    st.code(json_str, language='json')
        
        with tab2:
            st.subheader("Import data from JSON")
            
            uploaded_file = st.file_uploader("Upload JSON file", type=['json'])
            
            if uploaded_file is not None:
                try:
                    imported_data = json.load(uploaded_file)
                    
                    st.json(imported_data)
                    
                    if st.button("⚠️ Replace current data with imported data"):
                        st.session_state.data = imported_data
                        if save_yaml(imported_data, YAML_FILE):
                            st.success("✅ Data imported and saved successfully!")
                            st.rerun()
                except Exception as e:
                    st.error(f"Error importing JSON: {e}")

# Footer
st.markdown("---")
st.markdown("*DoYouBuzz Showcase Editor - Built with Streamlit*")
