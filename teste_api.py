import os
import requests
from dotenv import load_dotenv

# ---------------------------------------------------------
# 1. Configuração e Variáveis de Ambiente
# ---------------------------------------------------------
load_dotenv()

api_key = os.getenv("GOOGLE_MAPS_API_KEY")
url = "https://routes.googleapis.com/directions/v2:computeRoutes"

# ---------------------------------------------------------
# 2. Preparação da Requisição (Headers e Payload)
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# 3. Execução da Requisição
# ---------------------------------------------------------
resposta = requests.post(
    url,
    headers=headers,
    json=dados
)

print(resposta.status_code)
print(resposta.json())

# ---------------------------------------------------------
# 4. Extração de Dados da Resposta
# ---------------------------------------------------------
dados_resposta = resposta.json()
print(dados_resposta)

rotas = dados_resposta["routes"]
print(rotas)

rota = rotas[0]
print(rota)

distancia_metros = rota["distanceMeters"]
print(distancia_metros)

duracao = rota["duration"]
print(duracao)

static_duracao = rota["staticDuration"]
print(static_duracao)

# ---------------------------------------------------------
# 5. Conversões e Cálculos (Distância e Tempo)
# ---------------------------------------------------------
distancia_km = distancia_metros / 1000
print(f"Distância: {distancia_km} km")

duracao_sem_s = duracao.replace("s", "")
print(duracao_sem_s)

duracao_segundos = float(duracao_sem_s)
print(duracao_segundos)

tempo_atual_minutos = duracao_segundos / 60
print(f"Tempo atual: {tempo_atual_minutos:.2f} minutos")

static_duracao_sem_s = static_duracao.replace("s", "")
print(static_duracao_sem_s)

static_duracao_segundos = float(static_duracao_sem_s)
print(static_duracao_segundos)

tempo_normal_minutos = static_duracao_segundos / 60
print(f"Tempo normal: {tempo_normal_minutos:.2f} minutos")

# ---------------------------------------------------------
# 6. Indicadores de Trânsito
# ---------------------------------------------------------
percentual_transito = ((tempo_atual_minutos - tempo_normal_minutos) / tempo_normal_minutos) * 100
print(f"Variação do tempo: {percentual_transito:.2f}%")