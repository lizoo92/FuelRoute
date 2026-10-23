import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_MAPS_API_KEY")

url = "https://routes.googleapis.com/directions/v2:computeRoutes"

headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": api_key,
    "X-Goog-FieldMask": "routes.distanceMeters,routes.duration,routes.staticDuration"
}

dados = {
    "origin": {
        "address": "Avenida Paulista, 1106, São Paulo, SP"
    },
    "destination": {
        "address": "Rua Fradique Coutinho, 771, São Paulo, SP"
    },
    "travelMode": "DRIVE",
    "routingPreference": "TRAFFIC_AWARE"
}

resposta = requests.post(
    url,
    headers=headers,
    json=dados
)

print(resposta.status_code)
print(resposta.json())