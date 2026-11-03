VEICULO = {
    "nome": "Mercedes-Benz C180 Avantgarde",
    "ano": 2020,
    "fonte": "Inmetro PBE Veicular 2020",
    "consumos": {
        "gasolina": {"urbano": 10.3, "estrada": 14.6},
        "etanol": {"urbano": 7.2, "estrada": 10.1},
    },
}


def calcular_consumo(veiculo, combustivel, peso_urbano):
    urbano = veiculo["consumos"][combustivel]["urbano"]
    estrada = veiculo["consumos"][combustivel]["estrada"]

    litros_por_km = peso_urbano / urbano + (1 - peso_urbano) / estrada

    return 1 / litros_por_km


def ler_combustivel(veiculo):
    opcoes = list(veiculo["consumos"].keys())

    if len(opcoes) == 1:
        return opcoes[0]

    while True:
        escolha = input(
            f"Combustível no tanque ({' ou '.join(opcoes)}): "
        ).strip().lower()

        if escolha in opcoes:
            return escolha

        print(f"Opção inválida. Digite exatamente: {' ou '.join(opcoes)}.")


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


def converter_segundos_para_minutos(duracao):
    duracao_sem_s = duracao.replace("s", "")
    duracao_segundos = float(duracao_sem_s)
    duracao_minutos = duracao_segundos / 60
    return duracao_minutos


def classificar_transito(percentual_transito, veiculo, combustivel):
    if percentual_transito <= 0:
        peso_urbano = 0.0
        descricao_transito = "Sem trânsito"
    elif percentual_transito <= 15:
        peso_urbano = 0.35
        descricao_transito = "Trânsito leve"
    elif percentual_transito <= 50:
        peso_urbano = 0.70
        descricao_transito = "Trânsito moderado"
    else:
        peso_urbano = 1.0
        descricao_transito = "Trânsito intenso"

    consumo = calcular_consumo(veiculo, combustivel, peso_urbano)

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


def main():
    combustivel = ler_combustivel(VEICULO)

    distancia = float(input("Digite a distância da viagem em km: "))
    preco_combustivel = float(
        input(f"Digite o preço do {combustivel} em R$/L: ")
    )
    tempo_normal = float(input("Digite o tempo normal da rota em minutos: "))
    tempo_atual = float(input("Digite o tempo atual da rota em minutos: "))

    if validar_dados(distancia, preco_combustivel, tempo_normal, tempo_atual):
        percentual_transito = calcular_percentual_transito(
            tempo_normal,
            tempo_atual
        )

        consumo, descricao_transito = classificar_transito(
            percentual_transito,
            VEICULO,
            combustivel
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


if __name__ == "__main__":
    main()