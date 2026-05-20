import requests
import random
import feedparser
import os
from deep_translator import GoogleTranslator

# =========================
# CONFIG FACEBOOK
# =========================

PAGE_ID = "1073487005856687"
PAGE_TOKEN = "EAASlKZCWsRZBMBRkXVPGyOJuUwZCIhuIMyO5dxpiFMbH6XJRmqitnoXb5OTf9oAO8R20ATvpHWny0OnZBYqzkbgqvOZATjo2CvSKg3w4CDQPlAWIAZB6RcuBEbdzl1YO775MdHd8Gcy0HGJPZB6QHfB1m8ix0fzfhOBZBw7d4BRf2BZCbKAxzNtfeIY2uRCfxZC4WmLTkFvys45aO3kuLGaV2PKbZAbkleHPsSyglq7BtoZD"

# =========================
# SUBREDDITS
# =========================

subreddits = [
    "todayilearned",
    "Damnthatsinteresting",
    "interestingasfuck"
]

# =========================
# FILTRO DE CONTENIDO
# =========================

BAD_KEYWORDS = [
    "nsfw", "porn", "sex", "violence", "war", "racist", "kill"
]

USED_FILE = "used_posts.txt"


# =========================
# UTILIDADES
# =========================

def load_used():
    if not os.path.exists(USED_FILE):
        return set()
    return set(open(USED_FILE, "r", encoding="utf-8").read().splitlines())


def save_used(id_post):
    with open(USED_FILE, "a", encoding="utf-8") as f:
        f.write(id_post + "\n")


def is_valid(title):
    t = title.lower()
    return not any(word in t for word in BAD_KEYWORDS)


# =========================
# VIRAL STYLE REWRITE
# =========================

encabezados = [
    "🤯 ESTO ES REAL",
    "😳 DATO VIRAL",
    "🧠 CURIOSIDAD DEL DÍA",
    "🔥 INTERNET ESTÁ HABLANDO DE ESTO",
    "👀 MIRA ESTE DATO"
]


def make_message(title_es):
    encabezado = random.choice(encabezados)

    return f"""
{encabezado}

😳 {title_es}

👉 Esto parece falso… pero es completamente real.

¿Lo sabías? 👀

#Curiosidades #DatosCuriosos #ByteDiario
"""


# =========================
# IMAGEN (REDDIT FALLBACK)
# =========================

def get_image(post):
    # RSS no siempre trae imagen directa, fallback simple
    if hasattr(post, "media_content"):
        try:
            return post.media_content[0]["url"]
        except:
            pass
    return None


def generate_image_prompt(title):
    prompt = title.replace(" ", "%20")
    return f"https://image.pollinations.ai/prompt/viral%20curiosity%20fact%20{prompt}"


# =========================
# MAIN
# =========================

def run():

    used = load_used()

    subreddit = random.choice(subreddits)
    rss_url = f"https://www.reddit.com/r/{subreddit}/top/.rss?t=day"

    feed = feedparser.parse(rss_url)

    posts = [p for p in feed.entries if is_valid(p.title)]

    if not posts:
        print("❌ No hay posts válidos")
        return

    # quitar repetidos
    posts = [p for p in posts if p.id not in used]

    if not posts:
        print("♻️ Todos los posts ya fueron usados")
        return

    # elegir el más "viral" (RSS no tiene score real → simulamos)
    post = random.choice(posts)

    titulo_ingles = post.title

    # traducir
    titulo_es = GoogleTranslator(
        source='auto',
        target='es'
    ).translate(titulo_ingles)

    mensaje = make_message(titulo_es)

    # imagen
    image_url = get_image(post)
    if not image_url:
        image_url = generate_image_prompt(titulo_ingles)

    # =========================
    # PUBLICAR EN FACEBOOK
    # =========================

    url_fb = f"https://graph.facebook.com/{PAGE_ID}/photos"

    payload = {
        "url": image_url,
        "caption": mensaje,
        "access_token": PAGE_TOKEN
    }

    r = requests.post(url_fb, data=payload)

    # guardar usado
    save_used(post.id)

    print("===== RESULTADO =====")
    print(r.text)
    print("=====================")


if __name__ == "__main__":
    run()
