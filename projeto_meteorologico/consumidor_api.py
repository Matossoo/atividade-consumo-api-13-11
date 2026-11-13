"""Consumidor da API Meteorológica Offline.

Responsável por: montar a requisição, enviá-la à API local, verificar a
resposta, interpretar o JSON e devolver os dados organizados para a interface.
"""
import requests

# Endpoint local documentado (Anexo 2)
URL_API = "http://127.0.0.1:8000/v1/forecast"

# Localização definida na atividade: Jaraguá do Sul - SC
LOCALIDADE = "Jaraguá do Sul - SC"
LATITUDE = -26.4851
LONGITUDE = -49.0713


class ErroConsulta(Exception):
    """Falha ao consultar a API ou ao interpretar a resposta."""


def obter_dados_meteorologicos():
    """Consulta a API e retorna um dicionário com os dados atuais e as unidades."""
    # Parâmetros obrigatórios da API (nomes exatos da documentação)
    parametros = {"latitude": LATITUDE, "longitude": LONGITUDE}

    try:
        # GET com limite de espera, para não travar se a API não responder
        resposta = requests.get(URL_API, params=parametros, timeout=10)
        # Gera exceção se o status HTTP indicar erro (400, 404, 500...)
        resposta.raise_for_status()
        # Converte o corpo JSON em dicionário Python
        dados = resposta.json()
    except requests.exceptions.ConnectionError:
        raise ErroConsulta(
            "Não foi possível conectar à API em 127.0.0.1:8000. "
            "Verifique se o Uvicorn está em execução."
        )
    except requests.exceptions.Timeout:
        raise ErroConsulta("Tempo limite excedido ao aguardar a resposta da API.")
    except requests.exceptions.HTTPError as erro:
        raise ErroConsulta(f"A API retornou um erro HTTP: {erro}")
    except ValueError:
        raise ErroConsulta("A resposta da API não é um JSON válido.")

    try:
        # Os dados atuais ficam em "current"; as unidades em "current_units"
        atuais = dados["current"]
        unidades = dados["current_units"]
        # Seleciona apenas os campos exigidos pela avaliação
        return {
            "temperatura": atuais["temperature_2m"],
            "umidade_relativa": atuais["relative_humidity_2m"],
            "sensacao_termica": atuais["apparent_temperature"],
            "precipitacao": atuais["precipitation"],
            "velocidade_vento": atuais["wind_speed_10m"],
            "horario": atuais["time"],
            # Unidades vindas da própria API
            "unidades": {
                "temperatura": unidades["temperature_2m"],
                "umidade_relativa": unidades["relative_humidity_2m"],
                "sensacao_termica": unidades["apparent_temperature"],
                "precipitacao": unidades["precipitation"],
                "velocidade_vento": unidades["wind_speed_10m"],
            },
        }
    except (KeyError, TypeError) as erro:
        # Campo ausente ou estrutura inesperada
        raise ErroConsulta(f"Campo ausente ou estrutura inesperada na resposta: {erro}")


if __name__ == "__main__":
    # Teste independente do consumidor (sem a interface)
    print(obter_dados_meteorologicos())
