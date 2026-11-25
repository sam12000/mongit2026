"""Serveur MCP qui donne à Claude un outil pour interroger un LLM gratuit.

Claude reste le modèle principal ; il peut déléguer des tâches simples
(résumer, traduire, classer, deuxième avis...) à un LLM gratuit via l'outil
`ask_free_llm`.

Fournisseurs pris en charge (tous compatibles avec l'API OpenAI) :
groq, gemini, openrouter, mistral, ollama.
Choisir avec la variable FREE_LLM_PROVIDER (par défaut : groq).
"""

import os

from mcp.server.fastmcp import FastMCP
from openai import OpenAI

# Pour chaque fournisseur : adresse de l'API, variable de la clé, modèle par défaut.
PROVIDERS = {
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "key_env": "GROQ_API_KEY",
        "model": "llama-3.3-70b-versatile",
    },
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "key_env": "GEMINI_API_KEY",
        "model": "gemini-2.5-flash",
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "key_env": "OPENROUTER_API_KEY",
        "model": "meta-llama/llama-3.3-70b-instruct:free",
    },
    "mistral": {
        "base_url": "https://api.mistral.ai/v1",
        "key_env": "MISTRAL_API_KEY",
        "model": "mistral-small-latest",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "key_env": None,  # local : pas de clé nécessaire
        "model": "llama3.2",
    },
}

PROVIDER = os.environ.get("FREE_LLM_PROVIDER", "groq").lower()
if PROVIDER not in PROVIDERS:
    raise SystemExit(
        f"FREE_LLM_PROVIDER inconnu : {PROVIDER!r}. Choix : {', '.join(PROVIDERS)}"
    )

CONFIG = PROVIDERS[PROVIDER]
DEFAULT_MODEL = os.environ.get("FREE_LLM_MODEL", CONFIG["model"])

mcp = FastMCP("free-llm")


def _client() -> OpenAI:
    key_env = CONFIG["key_env"]
    if key_env is None:
        api_key = "ollama"
    else:
        api_key = os.environ.get(key_env)
        if not api_key:
            raise RuntimeError(
                f"Clé manquante : définissez la variable {key_env} "
                f"(fournisseur {PROVIDER})."
            )
    return OpenAI(base_url=CONFIG["base_url"], api_key=api_key)


@mcp.tool()
def ask_free_llm(
    prompt: str,
    system: str = "",
    model: str = "",
    temperature: float = 0.3,
    max_tokens: int = 1024,
) -> str:
    """Envoie une demande à un LLM gratuit et renvoie sa réponse texte.

    À utiliser pour des tâches simples à déléguer : résumé, traduction,
    reformulation, classement, extraction, ou pour obtenir un deuxième avis.

    Args:
        prompt: la demande à envoyer.
        system: consigne système facultative (rôle, style, format).
        model: modèle à utiliser ; vide = modèle par défaut du fournisseur.
        temperature: créativité (0 = précis, 1 = créatif).
        max_tokens: longueur maximale de la réponse.
    """
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        response = _client().chat.completions.create(
            model=model or DEFAULT_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except Exception as exc:  # renvoyer l'erreur à Claude plutôt que planter
        return f"Erreur du fournisseur {PROVIDER} : {exc}"

    return response.choices[0].message.content or ""


@mcp.tool()
def free_llm_info() -> str:
    """Indique quel fournisseur et quel modèle gratuits sont configurés."""
    return (
        f"Fournisseur : {PROVIDER}\n"
        f"Modèle par défaut : {DEFAULT_MODEL}\n"
        f"Adresse : {CONFIG['base_url']}"
    )


if __name__ == "__main__":
    mcp.run()
