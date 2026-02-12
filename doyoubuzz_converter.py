"""
DoYouBuzz JSON <-> Simplified YAML Converter
Maintains full compatibility with DoYouBuzz import/export
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any


def json_to_yaml(json_path: str, yaml_path: str) -> None:
    """Convert DoYouBuzz JSON to simplified YAML for editing"""
    with open(json_path, 'r', encoding='utf-8') as f:
        dyb_data = json.load(f)
    
    # Store original JSON for reference
    original_json_path = Path(yaml_path).with_suffix('.original.json')
    with open(original_json_path, 'w', encoding='utf-8') as f:
        json.dump(dyb_data, f, ensure_ascii=False, indent=2)
    
    # Build simplified structure with full metadata preservation
    showcase = {
        'personal_info': {
            'name': f"{dyb_data['owner']['firstname']} {dyb_data['owner']['lastname']}",
            'title': dyb_data['title']['value'],
            'email': dyb_data['owner']['login'],
            'phone': '',
            'location': dyb_data['contacts']['address'].get('country', ''),
            'website': dyb_data['owner']['url'],
            'linkedin': '',
            'github': ''
        },
        'summary': dyb_data['presentation']['text'],
        'skills': [],
        'experience': [],
        'certifications': [],
        'languages': [],
        # Preserve ALL DoYouBuzz metadata for perfect round-trip
        '_doyoubuzz_metadata': {
            'id': dyb_data.get('id'),
            'url': dyb_data.get('url'),
            'color': dyb_data.get('color'),
            'completion': dyb_data.get('completion'),
            'culture': dyb_data.get('culture'),
            'language': dyb_data.get('language'),
            'description': dyb_data.get('description'),
            'createdAt': dyb_data.get('createdAt'),
            'updatedAt': dyb_data.get('updatedAt'),
            'published': dyb_data.get('published'),
            'uploaded': dyb_data.get('uploaded'),
            'referenced': dyb_data.get('referenced'),
            'hidden': dyb_data.get('hidden'),
            'main': dyb_data.get('main'),
            'mainCvGroup': dyb_data.get('mainCvGroup'),
            'protected': dyb_data.get('protected'),
            'passwordProtected': dyb_data.get('passwordProtected'),
            'renderingMode': dyb_data.get('renderingMode'),
            'yearsExperience': dyb_data.get('yearsExperience'),
            'availability': dyb_data.get('availability'),
            'options': dyb_data.get('options'),
            'download': dyb_data.get('download'),
            'positions': dyb_data.get('positions'),
            'professionalPosition': dyb_data.get('professionalPosition'),
            'tags': dyb_data.get('tags'),
            'educations': dyb_data.get('educations'),
            'events': dyb_data.get('events'),
            'interests': dyb_data.get('interests'),
            'portfolios': dyb_data.get('portfolios'),
            # Preserve full owner and contacts objects (not just extracted fields)
            'owner_full': dyb_data.get('owner'),
            'contacts_full': dyb_data.get('contacts'),
            'presentation_full': dyb_data.get('presentation'),
            'title_full': dyb_data.get('title'),
            # Preserve skills as-is (too complex to edit, has many nested IDs)
            'skills_full': dyb_data.get('skills')
        }
    }
    
    # Convert skills
    for skill in dyb_data.get('skills', []):
        skill_category = {
            'category': skill['description'],
            'items': []
        }
        for child in skill.get('children', []):
            item = child['description']
            if 'level' in child and child.get('level'):
                item += f" ({child['level']}%)"
            skill_category['items'].append(item)
        
        if skill_category['items']:
            showcase['skills'].append(skill_category)
    
    # Convert experiences - store with DoYouBuzz IDs for round-trip
    for exp in dyb_data.get('experiences', []):
        # Extract missions
        missions = []
        for m in exp.get('missions', []):
            missions.append({
                'description': m['description'],
                '_dyb_id': m.get('id'),  # Preserve ID for round-trip
                '_dyb_sort': m.get('sort', 0)
            })
        
        # Extract results
        results = []
        for r in exp.get('results', []):
            results.append({
                'description': r['description'],
                '_dyb_id': r.get('id'),
                '_dyb_sort': r.get('sort', 0)
            })
        
        # Extract objectives
        objectives = []
        for o in exp.get('objectives', []):
            objectives.append({
                'description': o['description'],
                '_dyb_id': o.get('id'),
                '_dyb_sort': o.get('sort', 0)
            })
        
        # Extract context
        context = ''
        context_id = None
        if exp.get('contexts'):
            context = exp['contexts'][0].get('description', '')
            context_id = exp['contexts'][0].get('id')
        
        # Extract environments
        environments = []
        for env in exp.get('environments', []):
            environments.append({
                'description': env['description'],
                '_dyb_id': env.get('id'),
                '_dyb_sort': env.get('sort', 0)
            })
        
        experience_entry = {
            'title': exp.get('title', ''),
            'company': exp.get('company', ''),
            'location': exp.get('city', ''),
            'start_date': f"{exp['range']['start'].get('year', '')}-{exp['range']['start'].get('month', '').zfill(2) if exp['range']['start'].get('month') else ''}".rstrip('-'),
            'end_date': f"{exp['range']['end'].get('year', '')}-{exp['range']['end'].get('month', '').zfill(2) if exp['range']['end'].get('month') else ''}".rstrip('-'),
            'context': context,
            'missions': missions,
            'results': results,
            'objectives': objectives,
            'environments': environments,
            # Preserve ALL DoYouBuzz metadata for perfect round-trip
            '_dyb_id': exp.get('id'),
            '_dyb_context_id': context_id,
            '_dyb_sort': exp.get('sort', 0),
            '_dyb_views': exp.get('$views'),
            '_dyb_home': exp.get('home'),
            '_dyb_slug': exp.get('slug'),
            '_dyb_start': exp.get('start'),
            '_dyb_end': exp.get('end'),
            '_dyb_logo': exp.get('logo'),
            '_dyb_logos': exp.get('logos'),
            '_dyb_range_full': exp.get('range')  # Preserve full range object
        }
        
        showcase['experience'].append(experience_entry)
    
    # Convert certifications
    for cert in dyb_data.get('certificates', []):
        parts = cert['name'].split(' - ')
        name = parts[0] if len(parts) > 0 else cert['name']
        issuer = parts[1] if len(parts) > 1 else ''
        
        cert_entry = {
            'name': name,
            'issuer': issuer,
            'date': cert.get('obtainedAt', ''),
            'credential_url': '',
            # Preserve ALL metadata
            '_dyb_id': cert.get('id'),
            '_dyb_sort': cert.get('sort', 0),
            '_dyb_views': cert.get('$views'),
            '_dyb_full': cert  # Preserve entire object
        }
        showcase['certifications'].append(cert_entry)
    
    # Convert languages
    for lang in dyb_data.get('languageSkills', {}).get('elements', []):
        lang_map = {'en': 'Anglais', 'fr': 'Français', 'es': 'Espagnol', 'de': 'Allemand'}
        lang_code = lang.get('culture', '').split('_')[0]
        lang_name = lang_map.get(lang_code, lang_code.upper())
        
        lang_entry = {
            'language': lang_name,
            'proficiency': f"{lang.get('details', '')} ({lang.get('level', '')}%)".strip(),
            # Preserve ALL metadata
            '_dyb_id': lang.get('id'),
            '_dyb_culture': lang.get('culture'),
            '_dyb_level': lang.get('level'),
            '_dyb_details': lang.get('details'),
            '_dyb_sort': lang.get('sort'),
            '_dyb_full': lang  # Preserve entire object
        }
        showcase['languages'].append(lang_entry)
    
    # Save to YAML
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(showcase, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
    
    print(f"[OK] Converted {json_path} to {yaml_path}")
    print(f"[INFO] Original JSON saved to {original_json_path} for reference")


def yaml_to_json(yaml_path: str, json_path: str, original_json_path: str = None) -> None:
    """Convert simplified YAML back to DoYouBuzz JSON format"""
    with open(yaml_path, 'r', encoding='utf-8') as f:
        showcase = yaml.safe_load(f)
    
    # Start with metadata if available, otherwise load original or create minimal
    if '_doyoubuzz_metadata' in showcase:
        # Use preserved metadata as base
        meta = showcase['_doyoubuzz_metadata']
        dyb_data = {
            'id': meta.get('id'),
            'url': meta.get('url'),
            'color': meta.get('color'),
            'completion': meta.get('completion'),
            'culture': meta.get('culture'),
            'language': meta.get('language'),
            'description': meta.get('description'),
            'createdAt': meta.get('createdAt'),
            'updatedAt': meta.get('updatedAt'),
            'published': meta.get('published'),
            'uploaded': meta.get('uploaded'),
            'referenced': meta.get('referenced'),
            'hidden': meta.get('hidden'),
            'main': meta.get('main'),
            'mainCvGroup': meta.get('mainCvGroup'),
            'protected': meta.get('protected'),
            'passwordProtected': meta.get('passwordProtected'),
            'renderingMode': meta.get('renderingMode'),
            'yearsExperience': meta.get('yearsExperience'),
            'availability': meta.get('availability'),
            'options': meta.get('options'),
            'download': meta.get('download'),
            'positions': meta.get('positions'),
            'professionalPosition': meta.get('professionalPosition'),
            'tags': meta.get('tags'),
            'educations': meta.get('educations', []),
            'events': meta.get('events', []),
            'interests': meta.get('interests', []),
            'portfolios': meta.get('portfolios', []),
            'owner': meta.get('owner_full', {}),
            'contacts': meta.get('contacts_full', {}),
            'presentation': meta.get('presentation_full', {}),
            'title': meta.get('title_full', {}),
            'experiences': [],
            'skills': [],
            'certificates': [],
            'languageSkills': {"elements": []}
        }
    elif original_json_path and Path(original_json_path).exists():
        # Load original JSON as template
        with open(original_json_path, 'r', encoding='utf-8') as f:
            dyb_data = json.load(f)
    else:
        # Create minimal structure
        dyb_data = {
            "experiences": [],
            "skills": [],
            "certificates": [],
            "languageSkills": {"elements": []},
            "presentation": {"text": ""},
            "title": {"value": ""},
            "owner": {},
            "contacts": {"address": {}}
        }
    
    # Update personal info - only update editable fields, preserve metadata
    if 'personal_info' in showcase:
        pi = showcase['personal_info']
        names = pi.get('name', '').split(' ', 1)
        if 'owner' not in dyb_data:
            dyb_data['owner'] = {}
        dyb_data['owner']['firstname'] = names[0] if len(names) > 0 else ''
        dyb_data['owner']['lastname'] = names[1] if len(names) > 1 else ''
        dyb_data['owner']['login'] = pi.get('email', '')
        dyb_data['owner']['url'] = pi.get('website', '')
        
        if 'title' not in dyb_data:
            dyb_data['title'] = {}
        dyb_data['title']['value'] = pi.get('title', '')
        
        if 'contacts' not in dyb_data:
            dyb_data['contacts'] = {'address': {}}
        if 'address' not in dyb_data['contacts']:
            dyb_data['contacts']['address'] = {}
        dyb_data['contacts']['address']['country'] = pi.get('location', '')
    
    # Update summary - preserve other presentation fields
    if 'presentation' not in dyb_data:
        dyb_data['presentation'] = {}
    dyb_data['presentation']['text'] = showcase.get('summary', '')
    
    # Update experiences
    dyb_experiences = []
    for idx, exp in enumerate(showcase.get('experience', [])):
        # Parse dates (use preserved range if available, otherwise parse from simplified fields)
        if exp.get('_dyb_range_full'):
            range_obj = exp['_dyb_range_full']
        else:
            start_parts = exp.get('start_date', '').split('-')
            end_parts = exp.get('end_date', '').split('-')
            range_obj = {
                "start": {
                    "year": start_parts[0] if len(start_parts) > 0 else "",
                    "month": start_parts[1] if len(start_parts) > 1 else ""
                },
                "end": {
                    "year": end_parts[0] if len(end_parts) > 0 else "",
                    "month": end_parts[1] if len(end_parts) > 1 else ""
                }
            }
        
        dyb_exp = {
            "$views": exp.get('_dyb_views', []),
            "range": range_obj,
            "id": exp.get('_dyb_id', 19000000 + idx),
            "company": exp.get('company', ''),
            "city": exp.get('location', ''),
            "home": exp.get('_dyb_home', True),
            "sort": exp.get('_dyb_sort', idx),
            "title": exp.get('title', ''),
            "slug": exp.get('_dyb_slug', exp.get('company', '').lower().replace(' ', '-')),
            "missions": [],
            "results": [],
            "objectives": [],
            "contexts": [],
            "environments": []
        }
        
        # Preserve additional metadata fields if present
        if exp.get('_dyb_start'):
            dyb_exp['start'] = exp['_dyb_start']
        if exp.get('_dyb_end'):
            dyb_exp['end'] = exp['_dyb_end']
        if exp.get('_dyb_logo'):
            dyb_exp['logo'] = exp['_dyb_logo']
        if exp.get('_dyb_logos'):
            dyb_exp['logos'] = exp['_dyb_logos']
        
        # Add missions
        for mis_idx, mission in enumerate(exp.get('missions', [])):
            if isinstance(mission, dict):
                desc = mission.get('description', '')
                mis_id = mission.get('_dyb_id', 100000000 + idx * 100 + mis_idx)
                mis_sort = mission.get('_dyb_sort', mis_idx)
            else:
                desc = str(mission)
                mis_id = 100000000 + idx * 100 + mis_idx
                mis_sort = mis_idx
            
            dyb_exp['missions'].append({
                "toDel": False,
                "id": mis_id,
                "sort": mis_sort,
                "description": desc,
                "type": "mission"
            })
        
        # Add results
        for res_idx, result in enumerate(exp.get('results', [])):
            if isinstance(result, dict):
                desc = result.get('description', '')
                res_id = result.get('_dyb_id', 100000000 + idx * 100 + res_idx + 20)
                res_sort = result.get('_dyb_sort', res_idx)
            else:
                desc = str(result)
                res_id = 100000000 + idx * 100 + res_idx + 20
                res_sort = res_idx
            
            if desc:  # Only add non-empty results
                dyb_exp['results'].append({
                    "toDel": False,
                    "id": res_id,
                    "sort": res_sort,
                    "description": desc,
                    "type": "result"
                })
        
        # Add objectives
        for obj_idx, objective in enumerate(exp.get('objectives', [])):
            if isinstance(objective, dict):
                desc = objective.get('description', '')
                obj_id = objective.get('_dyb_id', 100000000 + idx * 100 + obj_idx + 30)
                obj_sort = objective.get('_dyb_sort', obj_idx)
            else:
                desc = str(objective)
                obj_id = 100000000 + idx * 100 + obj_idx + 30
                obj_sort = obj_idx
            
            if desc:  # Only add non-empty objectives
                dyb_exp['objectives'].append({
                    "toDel": False,
                    "id": obj_id,
                    "sort": obj_sort,
                    "description": desc,
                    "type": "objective"
                })
        
        # Add context
        if exp.get('context'):
            dyb_exp['contexts'].append({
                "toDel": False,
                "id": exp.get('_dyb_context_id', 100000000 + idx * 100),
                "sort": 0,
                "description": exp['context'],
                "type": "context"
            })
        
        # Add environments
        for env_idx, environment in enumerate(exp.get('environments', [])):
            if isinstance(environment, dict):
                desc = environment.get('description', '')
                env_id = environment.get('_dyb_id', 100000000 + idx * 100 + env_idx + 50)
                env_sort = environment.get('_dyb_sort', env_idx)
            else:
                desc = str(environment)
                env_id = 100000000 + idx * 100 + env_idx + 50
                env_sort = env_idx
            
            dyb_exp['environments'].append({
                "toDel": False,
                "id": env_id,
                "sort": env_sort,
                "description": desc,
                "type": "environment"
            })
        
        dyb_experiences.append(dyb_exp)
    
    dyb_data['experiences'] = dyb_experiences
    
    # Update certifications - preserve all metadata
    dyb_certs = []
    for idx, cert in enumerate(showcase.get('certifications', [])):
        # If we have the full preserved object, use it as-is (name/issuer not editable)
        if cert.get('_dyb_full'):
            cert_obj = cert['_dyb_full'].copy()
            # Only update the date field (editable)
            cert_obj['obtainedAt'] = cert.get('date', '')
            dyb_certs.append(cert_obj)
        else:
            # Create new certificate
            name = cert.get('name', '')
            issuer = cert.get('issuer', '')
            if issuer and issuer not in name:
                name = f"{name} - {issuer}"
            
            dyb_certs.append({
                "$views": cert.get('_dyb_views', []),
                "id": cert.get('_dyb_id', 1000000 + idx),
                "name": name,
                "obtainedAt": cert.get('date', ''),
                "sort": cert.get('_dyb_sort', idx)
            })
    
    dyb_data['certificates'] = dyb_certs
    
    # Update languages - preserve all metadata
    dyb_langs = []
    for idx, lang in enumerate(showcase.get('languages', [])):
        # If we have the full preserved object, use it
        if lang.get('_dyb_full'):
            dyb_langs.append(lang['_dyb_full'])
        else:
            # Create new language entry
            dyb_langs.append({
                "id": lang.get('_dyb_id', 2000000 + idx),
                "culture": lang.get('_dyb_culture', 'en'),
                "level": lang.get('_dyb_level', 95),
                "details": lang.get('_dyb_details', ''),
                "sort": lang.get('_dyb_sort', idx)
            })
    
    if dyb_langs:
        if 'languageSkills' not in dyb_data:
            dyb_data['languageSkills'] = {}
        dyb_data['languageSkills']['elements'] = dyb_langs
    
    # Restore skills from metadata (not editable in simplified view)
    if '_doyoubuzz_metadata' in showcase and showcase['_doyoubuzz_metadata'].get('skills_full'):
        dyb_data['skills'] = showcase['_doyoubuzz_metadata']['skills_full']
    
    # Save to JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(dyb_data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Converted {yaml_path} to {json_path}")
    print(f"[READY] Ready to import back to DoYouBuzz!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Convert JSON to YAML: python doyoubuzz_converter.py json2yaml <input.json> <output.yaml>")
        print("  Convert YAML to JSON: python doyoubuzz_converter.py yaml2json <input.yaml> <output.json> [original.json]")
        sys.exit(1)
    
    mode = sys.argv[1]
    
    if mode == "json2yaml":
        json_to_yaml(sys.argv[2], sys.argv[3])
    elif mode == "yaml2json":
        original = sys.argv[4] if len(sys.argv) > 4 else None
        yaml_to_json(sys.argv[2], sys.argv[3], original)
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)
