import requests
import random

PAGE_ID = "1073487005856687"
PAGE_TOKEN = "EAASlKZCWsRZBMBRkXVPGyOJuUwZCIhuIMyO5dxpiFMbH6XJRmqitnoXb5OTf9oAO8R20ATvpHWny0OnZBYqzkbgqvOZATjo2CvSKg3w4CDQPlAWIAZB6RcuBEbdzl1YO775MdHd8Gcy0HGJPZB6QHfB1m8ix0fzfhOBZBw7d4BRf2BZCbKAxzNtfeIY2uRCfxZC4WmLTkFvys45aO3kuLGaV2PKbZAbkleHPsSyglq7BtoZD"

curiosidades = [
    "El corazón de una ballena azul puede pesar más de 180 kilos.",
    "Los pulpos tienen tres corazones.",
    "La miel nunca se vence.",
    "Hay más estrellas en el universo que granos de arena en la Tierra.",
    "El cerebro humano genera suficiente electricidad para encender una bombilla."
]

post = random.choice(curiosidades)

mensaje = f"""🤯 DATO CURIOSO

{post}

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
