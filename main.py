import requests
import random
import feedparser
from deep_translator import GoogleTranslator

PAGE_ID = "1073487005856687"
PAGE_TOKEN = "EAASlKZCWsRZBMBRkXVPGyOJuUwZCIhuIMyO5dxpiFMbH6XJRmqitnoXb5OTf9oAO8R20ATvpHWny0OnZBYqzkbgqvOZATjo2CvSKg3w4CDQPlAWIAZB6RcuBEbdzl1YO775MdHd8Gcy0HGJPZB6QHfB1m8ix0fzfhOBZBw7d4BRf2BZCbKAxzNtfeIY2uRCfxZC4WmLTkFvys45aO3kuLGaV2PKbZAbkleHPsSyglq7BtoZD"

subreddits = [
    "todayilearned",
    "Damnthatsinteresting",
    "interestingasfuck"
]

subreddit = random.choice(subreddits)

rss_url = f"https://www.reddit.com/r/{subreddit}/top/.rss?t=day"

feed = feedparser.parse(rss_url)

post = random.choice(feed.entries)

titulo_ingles = post.title

titulo = GoogleTranslator(
    source='auto',
    target='es'
).translate(titulo_ingles)

encabezados = [
    "🤯 ESTO ES REAL",
    "😳 DATO VIRAL",
    "🧠 CURIOSIDAD DEL DÍA",
    "🔥 INTERNET ESTÁ HABLANDO DE ESTO",
    "👀 MIRA ESTE DATO"
]

encabezado = random.choice(encabezados)

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
