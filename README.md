# FuelRoute

O **FuelRoute** é um projeto em Python desenvolvido com o objetivo de calcular o consumo estimado de combustível e o custo de uma viagem considerando a distância da rota e as condições atuais de trânsito.

O projeto começou como uma calculadora simples com valores informados manualmente e vem evoluindo gradualmente para uma aplicação integrada à **Google Routes API**, capaz de utilizar dados reais de distância e duração de trajetos.

Além do desenvolvimento da aplicação, o FuelRoute também é utilizado como projeto prático de aprendizado de Python, APIs, Git/GitHub, organização de código e boas práticas de desenvolvimento.

---

## Objetivo

A aplicação deve permitir que o usuário informe:

- endereço de origem;
- endereço de destino;
- preço atual do combustível.

A partir desses dados, o FuelRoute consulta a Google Routes API e calcula:

- distância da rota;
- tempo atual da viagem;
- tempo de referência da rota;
- variação percentual do tempo;
- classificação das condições de trânsito;
- consumo estimado do veículo;
- quantidade estimada de combustível necessária;
- custo estimado da viagem.

---

# Estado atual do projeto

Atualmente, o FuelRoute já possui um fluxo funcional utilizando dados reais da Google Routes API.

Exemplo de utilização:

```text
Digite o endereço de origem: São Paulo
Digite o endereço de destino: Registro, São Paulo

Requisição realizada com sucesso.

Distância: 191.086 km
Tempo atual: 201.00 minutos
Tempo normal: 166.55 minutos
Variação do tempo: 20.68%

Classificação: Trânsito moderado
Consumo estimado: 9.00 km/L

Digite o preço do combustível em R$/L: 9.19

Litros necessários: 21.23 L
Custo da viagem: R$ 195.12
```

---

# Estrutura atual

O projeto está atualmente dividido principalmente em dois arquivos:

```text
FuelRoute/
│
├── fuelroute.py
├── teste_api.py
├── .env
└── .gitignore
```

## `fuelroute.py`

Concentra as principais funções responsáveis pela lógica da aplicação.

Atualmente possui funções para:

```python
validar_dados()
calcular_percentual_transito()
converter_segundos_para_minutos()
classificar_transito()
calcular_viagem()
exibir_resultado()
```

Também utiliza:

```python
if __name__ == "__main__":
    main()
```

para permitir que suas funções sejam importadas por outros módulos sem executar automaticamente o fluxo manual do programa.

---

## `teste_api.py`

É responsável atualmente pela integração com a Google Routes API.

O arquivo:

- carrega a chave da API;
- recebe origem e destino;
- monta a requisição;
- consulta a Google Routes API;
- verifica o código HTTP;
- valida se uma rota foi encontrada;
- extrai distância e duração;
- utiliza funções importadas de `fuelroute.py`;
- recebe o preço do combustível;
- calcula consumo e custo final.

---

# Google Routes API

O FuelRoute utiliza o endpoint:

```text
https://routes.googleapis.com/directions/v2:computeRoutes
```

A requisição utiliza atualmente:

```python
"travelMode": "DRIVE"
```

para rotas de automóvel e:

```python
"routingPreference": "TRAFFIC_AWARE"
```

para considerar as condições de trânsito.

Os principais dados solicitados à API são:

```text
routes.distanceMeters
routes.duration
routes.staticDuration
```

Representando respectivamente:

- distância da rota em metros;
- duração considerando as condições atuais;
- duração de referência da rota.

---

# Segurança da API Key

A chave da Google Routes API não é armazenada diretamente no código.

Ela é salva em:

```text
.env
```

no formato:

```text
GOOGLE_MAPS_API_KEY=CHAVE_DA_API
```

O arquivo `.env` está incluído no `.gitignore` para impedir que a chave seja enviada ao GitHub.

Exemplo:

```text
__pycache__/
*.pyc
.venv/
.env
.vscode/
```

A variável é carregada utilizando:

```python
from dotenv import load_dotenv
import os
```

e:

```python
load_dotenv()

api_key = os.getenv("GOOGLE_MAPS_API_KEY")
```

---

# Comunicação com a API

A biblioteca `requests` é utilizada para realizar a requisição HTTP:

```python
resposta = requests.post(
    url,
    headers=headers,
    json=dados
)
```

A aplicação verifica inicialmente o código HTTP:

```python
if resposta.status_code == 200:
    print("Requisição realizada com sucesso.")
else:
    print(f"Erro na requisição. Código: {resposta.status_code}")
    exit()
```

Também foi identificado durante os testes que uma requisição pode retornar HTTP `200` sem necessariamente possuir uma rota.

Por isso existe uma segunda validação:

```python
if "routes" not in dados_resposta:
    print("Nenhuma rota encontrada. Verifique os endereços informados.")
    exit()
```

Essa validação evita erros do tipo:

```text
KeyError: 'routes'
```

quando endereços inexistentes ou não reconhecidos são informados.

---

# Função de consulta da rota

A integração com a API começou a ser encapsulada na função:

```python
def obter_dados_rota(origem, destino):
```

Atualmente ela é responsável por:

```text
receber origem e destino
        ↓
montar o payload
        ↓
realizar a requisição HTTP
        ↓
validar a resposta
        ↓
verificar se existe uma rota
        ↓
extrair os dados necessários
        ↓
retornar distância e tempos
```

Seu retorno é:

```python
return distancia_metros, duracao, static_duracao
```

Permitindo utilizar:

```python
distancia_metros, duracao, static_duracao = obter_dados_rota(
    origem,
    destino
)
```

---

# Conversão da distância

A API retorna a distância em metros.

Exemplo:

```text
5438
```

A aplicação converte para quilômetros:

```python
distancia_km = distancia_metros / 1000
```

Resultado:

```text
5.438 km
```

---

# Conversão do tempo

A API retorna valores de duração no formato:

```text
"1275s"
```

Foi criada a função:

```python
def converter_segundos_para_minutos(duracao):
    duracao_sem_s = duracao.replace("s", "")
    duracao_segundos = float(duracao_sem_s)
    duracao_minutos = duracao_segundos / 60
    return duracao_minutos
```

O processo realizado é:

```text
"1275s"
↓
"1275"
↓
1275.0
↓
21.25 minutos
```

Essa mesma função é utilizada para `duration` e `staticDuration`.

---

# Cálculo da variação do tempo

A diferença entre o tempo atual e o tempo de referência da rota é calculada utilizando:

```python
percentual = (
    (tempo_atual - tempo_normal)
    / tempo_normal
) * 100
```

Exemplo:

```text
Tempo normal: 22.60 minutos
Tempo atual: 23.40 minutos

Variação: +3.54%
```

Uma variação negativa também é possível.

Exemplo:

```text
Tempo normal: 19.08 minutos
Tempo atual: 16.07 minutos

Variação: -15.81%
```

Nesse caso, a rota atual está mais rápida que o tempo de referência.

---

# Classificação do trânsito

As regras atuais do projeto são:

```text
Variação <= 0%   → Sem trânsito
Variação <= 15%  → Trânsito leve
Variação <= 50%  → Trânsito moderado
Variação > 50%   → Trânsito intenso
```

A função responsável é:

```python
classificar_transito()
```

---

# Consumo estimado

O veículo utilizado como referência inicial do projeto é uma **Mercedes-Benz C180 2020**.

As estimativas atuais são:

```text
Sem trânsito       → 10.5 km/L
Trânsito leve      → 9.8 km/L
Trânsito moderado  → 9.0 km/L
Trânsito intenso   → 8.0 km/L
```

Esses valores são hipóteses iniciais do projeto e poderão futuramente ser recalibrados utilizando dados reais de viagens.

---

# Cálculo de combustível

A quantidade estimada de combustível necessária é calculada por:

```python
litros_necessarios = distancia / consumo
```

Exemplo:

```text
Distância: 14.491 km
Consumo: 9.8 km/L

14.491 / 9.8 ≈ 1.48 L
```

---

# Cálculo do custo da viagem

O custo é calculado utilizando:

```python
custo_viagem = litros_necessarios * preco_combustivel
```

Exemplo:

```text
1.48 L × R$ 9.19/L ≈ R$ 13.59
```

---

# Entrada do preço do combustível

O programa aceita tanto o padrão:

```text
9.19
```

quanto:

```text
9,19
```

A vírgula é convertida para ponto antes da conversão:

```python
entrada_preco = entrada_preco.replace(",", ".")
```

Também existe tratamento para entradas inválidas:

```python
try:
    preco_combustivel = float(entrada_preco)
except ValueError:
    print("Preço inválido. Digite apenas números.")
    exit()
```

E valores menores ou iguais a zero são rejeitados:

```python
if preco_combustivel <= 0:
    print("O preço do combustível deve ser maior que zero.")
    exit()
```

---

# Modularização

Uma parte importante da evolução do FuelRoute foi separar responsabilidades em funções.

O projeto começou com cálculos executados diretamente e gradualmente passou a utilizar funções reutilizáveis.

Exemplos:

```python
calcular_percentual_transito()
classificar_transito()
calcular_viagem()
converter_segundos_para_minutos()
obter_dados_rota()
```

Também foi implementada a importação de funções entre módulos:

```python
from fuelroute import (
    calcular_percentual_transito,
    classificar_transito,
    converter_segundos_para_minutos,
    calcular_viagem
)
```

Isso permite manter a lógica principal em um único lugar e evitar duplicação de código.

---

# Git e GitHub

O projeto utiliza Git para controle de versão e GitHub como repositório remoto.

Fluxo utilizado entre desktop e notebook:

Antes de iniciar o desenvolvimento:

```bash
git pull
```

Depois das alterações:

```bash
git status
git add .
git commit -m "Descrição da alteração"
git push
```

Isso permite continuar o desenvolvimento entre diferentes computadores mantendo o projeto sincronizado.

---

# Ambiente de desenvolvimento

Ferramentas utilizadas atualmente:

- Python;
- Visual Studio Code;
- Git;
- GitHub;
- Google Cloud;
- Google Routes API;
- Requests;
- python-dotenv.

Bibliotecas Python principais:

```text
requests
python-dotenv
```

---

# Conceitos estudados durante o projeto

Até este ponto, o FuelRoute também serviu para praticar:

- variáveis;
- `input()`;
- conversão com `float()`;
- operadores matemáticos;
- `if`, `elif` e `else`;
- funções;
- parâmetros;
- `return`;
- múltiplos valores retornados;
- listas;
- dicionários;
- acesso a JSON;
- `try/except`;
- `ValueError`;
- escopo de variáveis;
- imports entre módulos;
- `if __name__ == "__main__"`;
- variáveis de ambiente;
- requisições HTTP;
- APIs REST;
- códigos HTTP;
- tratamento de respostas de APIs;
- Git;
- GitHub;
- `.gitignore`;
- organização e refatoração de código.

---

# Próximas etapas

As próximas melhorias planejadas incluem:

1. transformar a entrada e validação do preço em uma função própria;
2. continuar a modularização do código;
3. criar um fluxo principal com `main()`;
4. melhorar o tratamento de erros de conexão e API;
5. melhorar o tratamento de endereços ambíguos;
6. reorganizar a integração entre `fuelroute.py` e o módulo da API;
7. melhorar a apresentação do resultado;
8. criar uma interface utilizando Streamlit;
9. armazenar histórico de viagens;
10. utilizar SQLite;
11. analisar os dados de viagens com Pandas;
12. recalibrar as estimativas de consumo utilizando dados reais;
13. estudar aplicações futuras de Machine Learning;
14. realizar deploy da aplicação.

---

# Progresso estimado

Considerando o planejamento completo do FuelRoute, o projeto encontra-se atualmente em aproximadamente:

```text
40–45% do projeto total
```

Considerando apenas o MVP — consulta da rota, trânsito, consumo e custo — o desenvolvimento está aproximadamente em:

```text
70–75%
```

A aplicação já possui um fluxo funcional utilizando dados reais da Google Routes API, mas ainda existem etapas importantes de organização, robustez, interface, persistência de dados e análise.

---

## Status

```text
🟢 Lógica de cálculo
🟢 Classificação de trânsito
🟢 Integração com Google Routes API
🟢 Origem e destino informados pelo usuário
🟢 Distância e tempos reais
🟢 Entrada de preço do combustível
🟢 Cálculo de litros e custo
🟢 Tratamento básico de erros
🟡 Refatoração e modularização
⬜ Interface gráfica
⬜ Banco de dados
⬜ Histórico de viagens
⬜ Análise de dados
⬜ Machine Learning
⬜ Deploy
```

---

**Última atualização do progresso: 28 de outubro de 2026.**
