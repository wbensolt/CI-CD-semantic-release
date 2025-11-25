📝 Missions de veille

Mission 1 : Comprendre CI/CD (1h)


1. **Qu'est-ce que la CI (Continuous Integration) ?**
   - Quels problèmes résout-elle ?  l'objectif est de réduire le nombre d'erreurs humaines ainsi que d'accélérer le développement d'un code de qualité.
   - Quels sont les principes clés ? des commits fréquents, une automatisation complète, pipeline rapide
   - Donnez 3 exemples d'outils de CI : GitHub Actions, GitLab CI, Jenkins

2. **Qu'est-ce que le CD (Continuous Deployment/Delivery) ?**
   - Différence entre Continuous Delivery et Continuous Deployment ?
        + Continuous Delivery : Le code est toujours prêt à être déployé, mais un humain doit cliquer pour lancer le déploiement en production.
        + Continuous Deployment : Le déploiement en production est automatique sans intervention humaine
   - Quels sont les risques et bénéfices ?
        + Risques :
            . Mauvais tests → bugs en production
            . Mauvaise configuration du pipeline --> Peut casser le build pour tout le monde.
            . Coût en ressources : Les pipelines consomment CPU/mémoire (runners, VM).

3. **Pourquoi CI/CD est important ?**
   - Impact sur la qualité du code : Tests automatiques = moins de bugs / Static analysis (lint) = code propre / Build check = code qui compile toujours
   - Impact sur la vitesse de développement : Plus besoin de tester à la main / Merge rapide / Réduction du temps d’intégration
   - Impact sur la collaboration en équipe : Plus de conflits Git / Process normalisé (mêmes tests pour tout le monde) / Intégration continue = confiance entre développeurs

Mission 2 : Maîtriser uv

1. **Qu'est-ce que uv ?**
   - En quoi est-ce différent de pip/poetry/pipenv ?
        + pip (installation de packages)
        + pipenv / poetry (gestion d'environnements + dépendances)
   - Quels sont les avantages ? uv combine tout en un seul outil, avec des performances extrêmes (jusqu’à 10× plus rapides que pip/poetry).

2. **Comment uv fonctionne avec pyproject.toml ?**
   - Structure du fichier:
                            [project]
                            name = "my_app"
                            version = "0.1.0"
                            requires-python = ">=3.10"

                            dependencies = [
                                "fastapi>=0.110",
                                "uvicorn[standard]",
                                "pandas",
                            ]

                            [project.optional-dependencies]
                            dev = ["pytest", "ruff"]


   - Gestion des dépendances (séparé par sections):
                uv add fastapi → ajoute dans [project.dependencies]
                uv add pytest --group dev → ajoute dans [project.optional-dependencies.dev]
                uv sync → installe exactement ce que tu as dans pyproject.toml + uv.lock

   - Build backend
                uv est compatible avec tous les build-systems : setuptools, hatchling, poetry-core, maturin
                uv ne remplace pas le build-backend, il le supporte.

3. **Comment utiliser uv dans GitHub Actions ?**
   - Installation
   - Cache des dépendances
   - Exécution de commandes

Mission 3 : Comprendre Semantic Release (30min)


Qu'est-ce que le versionnage sémantique (SemVer) ?
    - Format MAJOR.MINOR.PATCH
        + MAJOR : changements incompatibles avec la version précédente (BREAKING CHANGE)
        + MINOR : ajout de nouvelles fonctionnalités rétrocompatibles
        + PATCH : corrections de bugs rétrocompatibles

    - Quand bumper chaque niveau ?
        + Rupture de compatibilité (BREAKING CHANGE)	MAJOR
        + Nouvelle fonctionnalité rétrocompatible	MINOR
        + Correction de bug rétrocompatible	PATCH

Qu'est-ce que Conventional Commits ?
    - Format des messages:
        <type>[scope optional][!]: <description>
        [corps optionnel]
        [pied optionnel]

    - Types de commits (feat, fix, etc.):
        feat: → nouvelle fonctionnalité → bump MINOR
        fix: → correction de bug → bump PATCH
        BREAKING CHANGE: dans le pied ou ! après type/étendue → bump MAJOR

    - Impact sur le versionnage
        Conventional Commits est une convention pour écrire des messages de commit clairs.
        Elle permet à des outils comme Python Semantic Release de déterminer automatiquement la prochaine version.

Comment python-semantic-release fonctionne ?

    Python Semantic Release (PSR) automatise le versionnage et la release.
    Étapes principales :
            Lire les commits → déterminer le bump (MAJOR, MINOR, PATCH)
            Mettre à jour la version dans les fichiers (ex: pyproject.toml)
            Construire les artifacts (wheel, sdist, etc.)
            Générer automatiquement le CHANGELOG
            Créer un tag et publier la release sur GitHub, GitLab, etc.

    - Configuration dans pyproject.toml
        Expemple:
                [tool.semantic_release]
                version_toml = ["pyproject.toml:project.version"]  # fichier à mettre à jour
                build_command = "python -m build --sdist --wheel ." # build artifacts
                commit_parser = "conventional"                     # parser pour Conventional Commits

                [tool.semantic_release.commit_parser_options]
                minor_tags = ["feat"]
                patch_tags = ["fix", "perf"]
                parse_squash_commits = true
                ignore_merge_commits = true

    - Génération du CHANGELOG:
        PSR lit les commits pour créer le CHANGELOG automatiquement
        Possibilité de filtrer les commits à inclure ou exclure, et de choisir le format (rst ou md)
        
        Exemple :
            [tool.semantic_release.changelog.default_templates]
            changelog_file = "docs/CHANGELOG.rst"
            output_format = "rst"

    - Création des releases GitHub:
        PSR peut créer automatiquement une release GitHub avec :
            le tag de version
            les notes de release (CHANGELOG)

Mission 5 : MkDocs & GitHub Pages

    - Comment MkDocs génère de la documentation ?
    **MkDocs** est un générateur de site statique conçu pour transformer des fichiers **Markdown** en un site web de documentation.

            ###  Fonctionnement

            1. Tu écris ta doc dans des fichiers `.md` (ex : `docs/index.md`, `docs/api.md`…).

            2. Tu configures ton site avec un fichier `mkdocs.yml` :

                * nom du projet
                * thème
                * structure du menu
                * extensions

            3. MkDocs convertit tout ça en site HTML via :

            ```
            mkdocs build
            ```

            Output → un dossier `site/` contenant le site statique.

            4. Pour le prévisualiser :

            ```
            mkdocs serve
            ```

            Cela démarre un serveur local avec live reload.

    - Comment déployer sur GitHub Pages ?

            ### 1️⃣ Activer Pages

                Dans **GitHub > Settings > Pages** :

                * Deployment → *GitHub Actions* (recommandé)

            ### 2️⃣ Utiliser le workflow officiel

            GitHub propose un workflow par défaut.

                ```yaml
                name: deploy-docs

                on:
                push:
                    branches: ["main"]

                permissions:
                contents: write

                jobs:
                build:
                    runs-on: ubuntu-latest
                    steps:
                    - uses: actions/checkout@v4

                    - name: Setup Python
                        uses: actions/setup-python@v5
                        with:
                        python-version: "3.12"

                    - name: Install MkDocs & theme
                        run: |
                        pip install mkdocs mkdocs-material mkdocstrings[python]

                    - name: Deploy to GitHub Pages
                        uses: peaceiris/actions-gh-pages@v4
                        with:
                        github_token: ${{ secrets.GITHUB_TOKEN }}
                        publish_dir: ./site
                ```

            Le processus :

                1. Build la doc
                2. Génère `/site`
                3. Déploie automatiquement vers GitHub Pages


    - Qu'est-ce que mkdocstrings ?

        `mkdocstrings` est une extension MkDocs permettant de **générer automatiquement la documentation de ton code**.

        ### Fonctionnement:
            * Tu écris des **docstrings Python** dans ton code.
            * `mkdocstrings` les analyse automatiquement.
            * Il génère des pages de documentation **dynamiquement** dans le site MkDocs.


## 📘 Documentation CI/CD : MkDocs, mkdocstrings & GitHub Pages

### 🔹 MkDocs

MkDocs génère un site statique à partir de fichiers Markdown. Le fichier `mkdocs.yml` définit le thème, la navigation et les extensions.
Commandes importantes :

* `mkdocs serve` → prévisualisation
* `mkdocs build` → génération du site (`/site`)

### 🔹 Déploiement sur GitHub Pages

* Activer Pages → *GitHub Actions*
* Utiliser un workflow qui :

  * installe MkDocs
  * génère `/site`
  * déploie avec `actions-gh-pages`

### 🔹 mkdocstrings

Extension MkDocs permettant de générer automatiquement la documentation à partir des docstrings du code Python.
S’intègre en Markdown via :

```
::: package.module
```

---

