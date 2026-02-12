# DoYouBuzz Showcase Editor

**Version 0.1.1**

Gestion et édition de CVs DoYouBuzz avec support multi-showcases. Éditez facilement vos informations professionnelles et créez des variantes de votre CV pour différents contextes.

## ✨ Fonctionnalités

### Édition complète du CV
- 👤 **Informations personnelles** : nom, titre, email, localisation
- 📝 **Résumé professionnel** : description éditable
- 🛠️ **Compétences** : gestion par catégories avec niveaux (0-100%)
- 💼 **Expériences professionnelles** :
  - Titre, entreprise, dates, localisation
  - Contexte détaillé du poste
  - Missions (actions réalisées)
  - Résultats (réalisations)
  - Environnement technique
- 🎓 **Certifications** : nom, organisme, date
- 🌍 **Langues** : langue et niveau de maîtrise

### Multi-showcases
- 📌 **Baseline** : CV de base (tracké dans Git)
- 📄 **Variants** : créez des versions adaptées (frontend, backend, data, etc.)
- 🔄 Basculez facilement entre showcases
- ♻️ Créez des variants à partir de n'importe quel showcase

### Import/Export
- 📥 Import JSON depuis DoYouBuzz
- 📤 Export JSON vers DoYouBuzz
- 💾 Sauvegarde automatique en YAML
- 🔄 Préservation des métadonnées DoYouBuzz

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.8+
- pip

### Installation
```bash
pip install -r requirements.txt
```

### Lancement
```bash
streamlit run app.py
```

L'application s'ouvre automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

## 📖 Utilisation

### Workflow classique

1. **Importer un CV DoYouBuzz**
   - Exportez votre CV depuis DoYouBuzz (format JSON)
   - Via CLI : `python doyoubuzz_converter.py json2yaml cv_doyoubuzz.json showcases/baseline.yaml`

2. **Éditer dans l'interface**
   - Lancez `streamlit run app.py`
   - Naviguez dans les sections (Personal Info, Summary, Skills, etc.)
   - Modifiez les champs
   - Cliquez sur "💾 Save to YAML" pour sauvegarder

3. **Créer des variants**
   - Dans la sidebar, section "➕ Create Variant"
   - Donnez un nom (ex: "frontend", "data-engineer")
   - Le variant est créé comme copie du showcase actuel
   - Éditez-le indépendamment

4. **Exporter vers DoYouBuzz**
   - Cliquez sur "📥 Export to DoYouBuzz JSON"
   - Un fichier `{showcase}_export.json` est généré
   - Importez-le dans DoYouBuzz
   - ⚠️ **Important** : Les résultats doivent être ajoutés manuellement dans DoYouBuzz (limitation de leur import JSON)

## 📁 Structure du projet

```
DC/
├── app.py                   # Interface Streamlit principale
├── doyoubuzz_converter.py   # Convertisseur bidirectionnel JSON ↔ YAML
├── showcase_manager.py      # Gestion des showcases (création, suppression)
├── requirements.txt         # Dépendances Python
├── .gitignore              # Fichiers à ignorer (exports, cache)
├── README.md               # Cette documentation
└── showcases/
    ├── baseline.yaml       # CV de base (tracké dans Git)
    └── *.yaml             # Variants (ignorés par Git)
```

## ⚠️ Limitations DoYouBuzz

**L'import JSON de DoYouBuzz ne supporte PAS :**
- ❌ **Résultats** : doivent être saisis manuellement dans l'interface DoYouBuzz
- ❌ **Objectifs** : non utilisés (supprimés de l'éditeur)

**Sections supportées par l'import JSON :**
- ✅ Informations personnelles
- ✅ Résumé professionnel
- ✅ Compétences avec niveaux
- ✅ Expériences (titre, entreprise, dates, contexte)
- ✅ Missions
- ✅ Environnement technique
- ✅ Certifications
- ✅ Langues

### Workaround pour les résultats

Pour copier facilement vos résultats dans DoYouBuzz :
```bash
python3 -c "
import yaml
with open('showcases/baseline.yaml') as f:
    data = yaml.safe_load(f)
for exp in data['experience']:
    if exp.get('results'):
        print(f\"\\n{exp['title']} - {exp['company']}\")
        for i, r in enumerate(exp['results'], 1):
            print(f'{i}. {r}')
"
```

## 🔧 Commandes CLI

### Convertir JSON → YAML
```bash
python doyoubuzz_converter.py json2yaml input.json output.yaml
```

### Convertir YAML → JSON
```bash
python doyoubuzz_converter.py yaml2json input.yaml output.json
```

## 🏗️ Métadonnées

Les métadonnées DoYouBuzz sont préservées via :
- `_dyb_*` : champs de métadonnées (IDs, sort, timestamps, etc.)
- `_doyoubuzz_metadata` : section complète des métadonnées globales

Cela garantit la **compatibilité round-trip** : YAML → JSON → DoYouBuzz → JSON → YAML

## 📝 Version

**v0.1.1** (2026-02-12)
- ✅ Multi-showcases (baseline + variants)
- ✅ Édition complète des sections principales
- ✅ Gestion des compétences avec niveaux
- ✅ Import/Export DoYouBuzz JSON
- ✅ Suppression du champ objectives (non supporté)
- ✅ Nettoyage du projet (788 KB)

## 📄 Licence

MIT

Co-Authored-By: Warp <agent@warp.dev>
