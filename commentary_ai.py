import urllib.request
import urllib.parse
import json

POLLINATIONS_BASE_URL = "https://text.pollinations.ai/"

def query_pollinations_ai(prompt: str, timeout: int = 8) -> str:
    """Queries Pollinations.ai free API for dynamic Pokémon battle commentary."""
    try:
        url = POLLINATIONS_BASE_URL + urllib.parse.quote(prompt)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8", errors="ignore").strip()
            # Clean up response quotes
            text = text.strip('"\'')
            return text
    except Exception as e:
        print(f"[pollinations] Note: {e} - using tactical fallback")
        return ""

def get_dynamic_pokemon_commentary(speaker: str, action: str, strategy: str, fallback_text: str) -> str:
    """
    Generates dynamic Pokémon challenge commentary using Pollinations AI,
    falling back to curated strategic script if unavailable.
    """
    if speaker == "Red":
        persona = "Trainer Red, a hyper-focused competitive Pokémon AI analyst executing an impossible Magikarp Solo Run"
    else:
        persona = "Champion Blue, the arrogant, shocked Pokémon League Champion losing his mind as his team gets swept"

    prompt = (
        f"You are {persona}. "
        f"Battle Action: {action}. Strategy: {strategy}. "
        f"In 1 to 2 intense, high-energy sentences, react to this turn. "
        f"No markdown, no emojis, no bullet points, just spoken words."
    )
    
    generated = query_pollinations_ai(prompt)
    if generated and len(generated) > 25 and len(generated) < 280:
        return generated
    
    return fallback_text
