distancia = float(input("Digite a distância da viagem em km: "))
preco_combustivel = float(input("Digite o preço do combustível em R$/L: "))
tempo_normal = float(input("Digite o tempo normal da rota em minutos: "))
tempo_atual = float(input("Digite o tempo atual da rota em minutos: "))

if distancia <= 0:
    print("A distância da viagem deve ser maior que zero.")
elif preco_combustivel <= 0:
    print("O preço do combustível deve ser maior que zero.")
elif tempo_normal <= 0:
    print("O tempo normal da rota deve ser maior que zero.")
elif tempo_atual <= 0:
    print("O tempo atual da rota deve ser maior que zero.")
else:
    percentual_transito = ((tempo_atual - tempo_normal) / tempo_normal) * 100

    if percentual_transito <= 10:
        consumo = 10.5
        descricao_transito = "Sem trânsito"
    elif percentual_transito <= 25:
        consumo = 9.8
        descricao_transito = "Trânsito leve"
    elif percentual_transito <= 50:
        consumo = 9.0
        descricao_transito = "Trânsito moderado"
    else:
        consumo = 8.0
        descricao_transito = "Trânsito intenso"

    litros_necessarios = distancia / consumo
    custo_viagem = litros_necessarios * preco_combustivel

    print("---Resultado da Viagem:---")
    print(f"Litros Necessários: {litros_necessarios:.2f} L")
    print(f"Custo da Viagem: R$ {custo_viagem:.2f}")
    print(f"Descrição do Trânsito: {descricao_transito}")
    print(f"Consumo Médio: {consumo:.1f} km/L")
    print(f"Variação no tempo da rota: {percentual_transito:.1f}%")
