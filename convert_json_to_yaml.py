import json
import yaml
from pathlib import Path

# Load the JSON file
json_file = Path("/Users/lss/Downloads/cv-JEMS-LSI-Expert-Plateformes-Data-amp-Big-Data-mdash-Environnements-Critiques-amp-Cloud.json")
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Build the showcase structure
showcase = {
    'personal_info': {
        'name': f"{data['owner']['firstname']} {data['owner']['lastname']}",
        'title': data['title']['value'],
        'email': data['owner']['login'],
        'phone': '',
        'location': data['contacts']['address']['country'],
        'website': data['owner']['url'],
        'linkedin': '',
        'github': ''
    },
    'summary': data['presentation']['text'],
    'skills': [],
    'experience': [],
    'education': [],
    'projects': [],
    'certifications': [],
    'languages': []
}

# Convert skills
for skill in data['skills']:
    skill_category = {
        'category': skill['description'],
        'items': []
    }
    for child in skill.get('children', []):
        item = child['description']
        if 'level' in child and child['level']:
            item += f" ({child['level']}%)"
        skill_category['items'].append(item)
    
    if skill_category['items']:
        showcase['skills'].append(skill_category)

# Convert experiences
for exp in data['experiences']:
    # Extract missions
    missions = [m['description'] for m in exp.get('missions', [])]
    
    # Extract context (take first if exists)
    context = ''
    if exp.get('contexts'):
        context = exp['contexts'][0].get('description', '')
    
    # Extract environments
    environments = [env['description'] for env in exp.get('environments', [])]
    
    experience_entry = {
        'title': exp.get('title', ''),
        'company': exp.get('company', ''),
        'location': exp.get('city', ''),
        'start_date': f"{exp['range']['start'].get('year', '')}-{exp['range']['start'].get('month', '01') if exp['range']['start'].get('month') else ''}".rstrip('-'),
        'end_date': f"{exp['range']['end'].get('year', '')}-{exp['range']['end'].get('month', '01') if exp['range']['end'].get('month') else ''}".rstrip('-'),
        'context': context,
        'missions': missions,
        'environments': environments
    }
    
    showcase['experience'].append(experience_entry)

# Convert certifications
for cert in data['certificates']:
    cert_entry = {
        'name': cert['name'],
        'issuer': cert['name'].split(' - ')[-1] if ' - ' in cert['name'] else '',
        'date': cert.get('obtainedAt', ''),
        'credential_url': ''
    }
    # Clean up the name if issuer was extracted
    if ' - ' in cert_entry['name']:
        cert_entry['name'] = cert_entry['name'].rsplit(' - ', 1)[0]
    
    showcase['certifications'].append(cert_entry)

# Convert languages
for lang in data['languageSkills']['elements']:
    lang_entry = {
        'language': lang['culture'].split('_')[0].upper(),
        'proficiency': f"{lang.get('details', '')} ({lang.get('level', '')}%)"
    }
    showcase['languages'].append(lang_entry)

# Save to YAML
output_file = Path("showcase.yaml")
with open(output_file, 'w', encoding='utf-8') as f:
    yaml.dump(showcase, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)

print(f"✅ Converted JSON to {output_file}")
