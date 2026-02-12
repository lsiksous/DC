# Contributing to DoYouBuzz Showcase Editor

Merci de votre intérêt pour contribuer au projet ! 🎉

## 🌿 Git Workflow

Nous utilisons **Git Flow** :

- `main` : Production (releases stables)
- `develop` : Développement (intégration)
- `feature/*` : Nouvelles fonctionnalités
- `bugfix/*` : Corrections de bugs
- `chore/*` : Maintenance et configuration

### Créer une branche

```bash
# Feature
git checkout develop
git checkout -b feature/nom-de-la-feature

# Bugfix
git checkout develop
git checkout -b bugfix/nom-du-bug

# Chore
git checkout develop
git checkout -b chore/nom-de-la-tache
```

## 📝 Conventions de commits

Nous suivons [Conventional Commits](https://www.conventionalcommits.org/) :

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage, missing semi colons, etc
- `refactor`: Refactoring de code
- `test`: Ajout de tests
- `chore`: Tâches de maintenance

### Exemples
```bash
feat(showcase): add duplicate showcase feature
fix(export): correct JSON format for DoYouBuzz import
docs(readme): update installation instructions
chore(deps): update streamlit to v1.30.0
```

## 🔄 Pull Request Process

1. **Créez votre branche** depuis `develop`
2. **Développez** votre fonctionnalité
3. **Testez** localement
4. **Commitez** avec des messages conventionnels
5. **Push** votre branche
6. **Ouvrez une PR** vers `develop`
7. **Attendez la review**

### Template PR
```markdown
## Description
Décrivez les changements

## Type de changement
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Tests
- [ ] Testé localement
- [ ] App démarre sans erreur
- [ ] Import/Export fonctionnel

## Checklist
- [ ] Code suit les conventions
- [ ] CHANGELOG.md mis à jour
- [ ] Documentation mise à jour
```

## 🧪 Tests

Avant de soumettre une PR :

```bash
# Lancer l'app
streamlit run app.py

# Tester l'import/export
python doyoubuzz_converter.py json2yaml test.json test.yaml
python doyoubuzz_converter.py yaml2json test.yaml test_out.json
```

## 📚 Documentation

- Mettez à jour `README.md` pour les nouvelles fonctionnalités
- Ajoutez vos changements dans `CHANGELOG.md`
- Documentez les fonctions complexes avec des docstrings

## 🐛 Signaler un bug

Utilisez les [GitHub Issues](https://github.com/lsiksous/DC/issues) avec le template bug.

## 💡 Proposer une fonctionnalité

Utilisez les [GitHub Issues](https://github.com/lsiksous/DC/issues) avec le template feature request.

## 📋 Style de code

- Python : PEP 8
- Indentation : 4 espaces
- Line length : 100 caractères max
- Noms de variables : snake_case
- Noms de fonctions : snake_case
- Noms de classes : PascalCase

## 🙏 Attribution

Tous les commits incluent :
```
Co-Authored-By: Warp <agent@warp.dev>
```

Merci pour votre contribution ! 🚀
