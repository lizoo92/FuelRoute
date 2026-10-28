import os
import requests
from dotenv import load_dotenv
from fuelroute import (
    calcular_percentual_transito,
    classificar_transito,
    converter_segundos_para_minutos
)

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

tempo_normal_minutos = converter_segundos_para_minutos(static_duracao)
tempo_atual_minutos = converter_segundos_para_minutos(duracao)

print(f"Tempo atual: {tempo_atual_minutos:.2f} minutos")
print(f"Tempo normal: {tempo_normal_minutos:.2f} minutos")
# ---------------------------------------------------------
# 6. Indicadores de Trânsito
# ---------------------------------------------------------
percentual_variacao_tempo = calcular_percentual_transito(
    tempo_normal_minutos,
    tempo_atual_minutos
)
print(f"Variação do tempo: {percentual_variacao_tempo:.2f}%")

# ---------------------------------------------------------
# 7. Classificação do Trânsito
# ---------------------------------------------------------

consumo, descricao_transito = classificar_transito(
    percentual_variacao_tempo
)

print(f"Classificação: {descricao_transito}")
print(f"Consumo estimado: {consumo:.2f} km/L")