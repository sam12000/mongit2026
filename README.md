# free-llm : donner à Claude un LLM gratuit comme outil

Claude reste le modèle principal. Ce petit serveur MCP lui ajoute un outil
`ask_free_llm` pour **déléguer des tâches simples** (résumer, traduire,
reformuler, classer, deuxième avis) à un LLM **gratuit**.

> Analogie : Claude est le chef de projet ; le LLM gratuit est un assistant
> à qui il confie les tâches répétitives.

## Fournisseurs pris en charge

| `FREE_LLM_PROVIDER` | Clé à définir        | Modèle par défaut                         | Où obtenir la clé          |
|---------------------|----------------------|-------------------------------------------|----------------------------|
| `groq` (défaut)     | `GROQ_API_KEY`       | `llama-3.3-70b-versatile`                 | console.groq.com           |
| `gemini`            | `GEMINI_API_KEY`     | `gemini-2.5-flash`                        | aistudio.google.com        |
| `openrouter`        | `OPENROUTER_API_KEY` | `meta-llama/llama-3.3-70b-instruct:free`  | openrouter.ai              |
| `mistral`           | `MISTRAL_API_KEY`    | `mistral-small-latest`                    | console.mistral.ai         |
| `ollama` (local)    | aucune               | `llama3.2`                                | ollama.com                 |

Les modèles gratuits et les quotas changent souvent. Si un modèle n'existe
plus, changez-le avec `FREE_LLM_MODEL`.

## Installation (étape par étape)

1. **Cloner le dépôt et installer les dépendances**
   ```bash
   git clone https://github.com/sam12000/mongit2026.git
   cd mongit2026
   pip install -r requirements.txt
   ```

2. **Créer une clé gratuite** chez un fournisseur (par exemple Groq).

3. **Exporter la clé dans votre terminal** (ne jamais l'écrire dans un fichier commité)
   ```bash
   export FREE_LLM_PROVIDER=groq
   export GROQ_API_KEY="votre_cle"
   ```
   Pour la rendre permanente, ajoutez ces lignes à `~/.bashrc` ou `~/.zshrc`.

4. **Lancer Claude Code depuis le dossier du dépôt**
   ```bash
   claude
   ```
   Le fichier `.mcp.json` déclare le serveur `free-llm`. Claude Code vous
   demande de l'approuver la première fois. Vérifiez avec `/mcp`.

### Variante : l'ajouter pour tous vos projets

```bash
claude mcp add free-llm --scope user \
  -e FREE_LLM_PROVIDER=groq -e GROQ_API_KEY="votre_cle" \
  -- python3 /chemin/vers/mongit2026/free_llm_mcp.py
```

## Utilisation : exemples de demandes à Claude

- « Demande à `ask_free_llm` de résumer ce fichier en 5 points. »
- « Utilise le LLM gratuit pour traduire ce README en anglais. »
- « Demande un deuxième avis au LLM gratuit sur cette fonction. »
- « Quel LLM gratuit est configuré ? » (appelle `free_llm_info`)

## Outils exposés

| Outil           | Paramètres                                                    | Rôle                               |
|-----------------|---------------------------------------------------------------|------------------------------------|
| `ask_free_llm`  | `prompt`, `system`, `model`, `temperature`, `max_tokens`      | Envoie la demande, renvoie le texte |
| `free_llm_info` | aucun                                                         | Affiche fournisseur et modèle       |

## Dépannage

- **« Clé manquante »** : la variable de clé du fournisseur n'est pas définie
  dans le terminal d'où vous lancez `claude`.
- **Erreur 429** : quota gratuit atteint. Attendez, ou changez de fournisseur.
- **Modèle introuvable** : définissez `FREE_LLM_MODEL` avec un modèle actuel.
- **Ollama** : lancez `ollama serve` et `ollama pull llama3.2` avant.

## Sécurité

- Les clés ne sont lues que depuis les variables d'environnement.
- `.env` est ignoré par git ; `.env.example` sert de modèle sans clé.
- Ce que vous envoyez au LLM gratuit part chez ce fournisseur : n'y mettez
  pas de données sensibles (les offres gratuites peuvent servir à
  l'entraînement de leurs modèles).
