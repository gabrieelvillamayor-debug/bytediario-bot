import os
import requests
from openai import OpenAI

PAGE_ID = "1073487005856687"
PAGE_TOKEN = "EAASlKZCWsRZBMBRkXVPGyOJuUwZCIhuIMyO5dxpiFMbH6XJRmqitnoXb5OTf9oAO8R20ATvpHWny0OnZBYqzkbgqvOZATjo2CvSKg3w4CDQPlAWIAZB6RcuBEbdzl1YO775MdHd8Gcy0HGJPZB6QHfB1m8ix0fzfhOBZBw7d4BRf2BZCbKAxzNtfeIY2uRCfxZC4WmLTkFvys45aO3kuLGaV2PKbZAbkleHPsSyglq7BtoZD"

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

prompt = """
Genera un post viral de curiosidad para Facebook.

FORMATO:
- título impactante
- texto corto
- pregunta final
- hashtags

ESTILO:
viral, humano, curioso, atrapante.

NO repitas curiosidades comunes.
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

mensaje = response.choices[0].message.content

url = f"https://graph.facebook.com/{PAGE_ID}/feed"

payload = {
    "message": mensaje,
    "access_token": PAGE_TOKEN
}

r = requests.post(url, data=payload)

print(r.text)
