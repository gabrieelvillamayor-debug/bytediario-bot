import requests
import random

PAGE_ID = "1073487005856687"
PAGE_TOKEN = "EAASlKZCWsRZBMBRkXVPGyOJuUwZCIhuIMyO5dxpiFMbH6XJRmqitnoXb5OTf9oAO8R20ATvpHWny0OnZBYqzkbgqvOZATjo2CvSKg3w4CDQPlAWIAZB6RcuBEbdzl1YO775MdHd8Gcy0HGJPZB6QHfB1m8ix0fzfhOBZBw7d4BRf2BZCbKAxzNtfeIY2uRCfxZC4WmLTkFvys45aO3kuLGaV2PKbZAbkleHPsSyglq7BtoZD"

# Obtener curiosidad random
fact = requests.get(
    "https://uselessfacts.jsph.pl/api/v2/facts/random"
).json()

dato = fact["text"]

titulos = [
    "🤯 DATO QUE TE VOLARÁ LA CABEZA",
    "😳 ESTO ES REAL",
    "🧠 CURIOSIDAD DEL DÍA",
    "👀 CASI NADIE SABE ESTO",
    "🔥 DATO IMPACTANTE"
]

titulo = random.choice(titulos)

mensaje = f"""
{titulo}

{dato}

¿Lo sabías? 👀

#Curiosidades #DatosCuriosos #SabiasQue #ByteDiario
"""

url = f"https://graph.facebook.com/{PAGE_ID}/feed"

payload = {
    "message": mensaje,
    "access_token": PAGE_TOKEN
}

r = requests.post(url, data=payload)

print(r.text)
