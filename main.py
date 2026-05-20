import requests
import random
from deep_translator import GoogleTranslator

PAGE_ID = "1073487005856687"
PAGE_TOKEN = "EAASlKZCWsRZBMBRkXVPGyOJuUwZCIhuIMyO5dxpiFMbH6XJRmqitnoXb5OTf9oAO8R20ATvpHWny0OnZBYqzkbgqvOZATjo2CvSKg3w4CDQPlAWIAZB6RcuBEbdzl1YO775MdHd8Gcy0HGJPZB6QHfB1m8ix0fzfhOBZBw7d4BRf2BZCbKAxzNtfeIY2uRCfxZC4WmLTkFvys45aO3kuLGaV2PKbZAbkleHPsSyglq7BtoZD"

headers = {
    "User-Agent": "Mozilla/5.0"
}

subreddits = [
    "todayilearned",
    "Damnthatsinteresting",
    "interestingasfuck"
]

subreddit = random.choice(subreddits)

url_reddit = f"https://www.reddit.com/r/{subreddit}/top.json?t=day&limit=15"

response = requests.get(
    url_reddit,
    headers=headers
)

print(response.status_code)

data = response.json()

posts = data["data"]["children"]

post_random = random.choice(posts)

titulo_ingles = post_random["data"]["title"]

titulo = GoogleTranslator(
    source='auto',
    target='es'
).translate(titulo_ingles)

mensajes = [
    "🤯 ESTO ES REAL",
    "🧠 DATO VIRAL DEL DÍA",
    "😳 CASI NADIE SABE ESTO",
    "🔥 INTERNET ESTÁ HABLANDO DE ESTO",
    "👀 MIRA ESTE DATO"
]

encabezado = random.choice(mensajes)

mensaje = f"""
{encabezado}

{titulo}

¿Lo sabías? 👀

#Curiosidades #DatosCuriosos #ByteDiario
"""

url_fb = f"https://graph.facebook.com/{PAGE_ID}/feed"

payload = {
    "message": mensaje,
    "access_token": PAGE_TOKEN
}

r = requests.post(url_fb, data=payload)

print(r.text)

