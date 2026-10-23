def validar_dados(distancia, preco_combustivel, tempo_normal, tempo_atual):
    if distancia <= 0:
        print("A distância da viagem deve ser maior que zero.")
        return False
    if preco_combustivel <= 0:
        print("O preço do combustível deve ser maior que zero.")
        return False
    if tempo_normal <= 0:
        print("O tempo normal da rota deve ser maior que zero.")
        return False
    if tempo_atual <= 0:
        print("O tempo atual da rota deve ser maior que zero.")
        return False
    return True


def calcular_percentual_transito(tempo_normal, tempo_atual):
    percentual = ((tempo_atual - tempo_normal) / tempo_normal) * 100
    return percentual


def classificar_transito(percentual_transito):
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

    return consumo, descricao_transito


def calcular_viagem(distancia, consumo, preco_combustivel):
    litros_necessarios = distancia / consumo
    custo_viagem = litros_necessarios * preco_combustivel
    return litros_necessarios, custo_viagem


def exibir_resultado(
    litros_necessarios,
    custo_viagem,
    descricao_transito,
    consumo,
    percentual_transito
):
    print(f"\nDescrição do trânsito: {descricao_transito}")
    print(f"Percentual de trânsito: {percentual_transito:.2f}%")
    print(f"Consumo médio do veículo: {consumo:.2f} km/L")
    print(f"Litros necessários para a viagem: {litros_necessarios:.2f} L")
    print(f"Custo total da viagem: R$ {custo_viagem:.2f}")

distancia = float(input("Digite a distância da viagem em km: "))
preco_combustivel = float(input("Digite o preço do combustível em R$/L: "))
tempo_normal = float(input("Digite o tempo normal da rota em minutos: "))
tempo_atual = float(input("Digite o tempo atual da rota em minutos: "))

if validar_dados(distancia, preco_combustivel, tempo_normal, tempo_atual):
    percentual_transito = calcular_percentual_transito(
        tempo_normal,
        tempo_atual
    )

    consumo, descricao_transito = classificar_transito(
        percentual_transito
    )

    litros_necessarios, custo_viagem = calcular_viagem(
        distancia,
        consumo,
        preco_combustivel
    )

    exibir_resultado(
        litros_necessarios,
        custo_viagem,
        descricao_transito,
        consumo,
        percentual_transito
    )