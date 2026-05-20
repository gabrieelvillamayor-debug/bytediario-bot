import requests
import random
import feedparser
import os
from deep_translator import GoogleTranslator
from datetime import datetime

PAGE_ID = "1073487005856687"
PAGE_TOKEN = "EAASlKZCWsRZBMBRkXVPGyOJuUwZCIhuIMyO5dxpiFMbH6XJRmqitnoXb5OTf9oAO8R20ATvpHWny0OnZBYqzkbgqvOZATjo2CvSKg3w4CDQPlAWIAZB6RcuBEbdzl1YO775MdHd8Gcy0HGJPZB6QHfB1m8ix0fzfhOBZBw7d4BRf2BZCbKAxzNtfeIY2uRCfxZC4WmLTkFvys45aO3kuLGaV2PKbZAbkleHPsSyglq7BtoZD"

subreddits = [
    "todayilearned",
    "Damnthatsinteresting",
    "interestingasfuck"
]

USED_FILE = "used_posts.txt"

BAD_KEYWORDS = [
    "nsfw", "porn", "sex", "violence", "war", "racist", "kill"
]

# =========================
# HORARIO (UTC GITHUB)
# =========================

def get_tipo():
    hour = datetime.utcnow().hour

    if hour == 12:
        return "mañana"
    elif hour == 18:
        return "siesta"
    elif hour == 23:
        return "tarde"
    else:
        return "random"


# =========================
# UTILIDADES
# =========================

def load_used():
    if not os.path.exists(USED_FILE):
        return set()
    return set(open(USED_FILE, "r", encoding="utf-8").read().splitlines())


def save_used(post_id):
    with open(USED_FILE, "a", encoding="utf-8") as f:
        f.write(post_id + "\n")


def is_valid(title):
    t = title.lower()
    return not any(w in t for w in BAD_KEYWORDS)


# =========================
# ESTILO VIRAL SEGÚN HORARIO
# =========================

def make_message(text, tipo):

    if tipo == "mañana":
        header = "🌅 CURIOSIDAD DEL DÍA"
        hook = "🧠 Esto es más interesante de lo que parece:"
        end = "¿Lo sabías?"
        tags = "#Curiosidades #Datos"

    elif tipo == "siesta":
        header = "😳 DATO IMPACTANTE"
        hook = "🔥 Esto te va a sorprender:"
        end = "Increíble pero real."
        tags = "#Viral #Increíble"

    elif tipo == "tarde":
        header = "🤯 INTERNET NO LO PUEDE CREER"
        hook = "⚠️ Nadie habla de esto:"
        end = "Esto cambia todo."
        tags = "#Misterio #Curiosidades"

    else:
        header = "👀 DATO CURIOSO"
        hook = "👉 Atención:"
        end = "¿Lo sabías?"
        tags = "#DatosCuriosos"

    return f"""
{header}

{hook}

😳 {text}

{end}

{tags}
"""


# =========================
# MAIN
# =========================

def run():

    tipo = get_tipo()
    used = load_used()

    subreddit = random.choice(subreddits)
    rss_url = f"https://www.reddit.com/r/{subreddit}/top/.rss?t=day"

    feed = feedparser.parse(rss_url)

    posts = [p for p in feed.entries if is_valid(p.title)]
    posts = [p for p in posts if p.id not in used]

    if not posts:
        print("❌ No hay posts disponibles")
        return

    post = random.choice(posts)

    titulo_es = GoogleTranslator(
        source='auto',
        target='es'
    ).translate(post.title)

    mensaje = make_message(titulo_es, tipo)

    # Imagen (simple fallback)
    image_url = None

    if hasattr(post, "media_content"):
        try:
            image_url = post.media_content[0]["url"]
        except:
            pass

    if not image_url:
        image_url = f"https://image.pollinations.ai/prompt/viral%20curiosity%20{post.title.replace(' ','%20')}"

    # FACEBOOK POST
    url_fb = f"https://graph.facebook.com/{PAGE_ID}/photos"

    payload = {
        "url": image_url,
        "caption": mensaje,
        "access_token": PAGE_TOKEN
    }

    r = requests.post(url_fb, data=payload)

    save_used(post.id)

    print(r.text)


if __name__ == "__main__":
    run()
