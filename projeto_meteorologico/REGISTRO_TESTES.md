# Registro de testes

Ambiente: Python 3.12.3, Git 2.43.0, requests 2.34.2, streamlit 1.67.0. API em `127.0.0.1:8000`.

## Análise dos requisitos
Exibir: temperatura (°C), umidade (%), sensação térmica (°C), precipitação (mm), vento (km/h) e horário da API. Parâmetros: `latitude=-26.4851`, `longitude=-49.0713`. Dados em `current` e `current_units`.

## Teste da requisição à API (equivalente ao Postman — curl, GET)
| Requisição | Resultado |
|---|---|
| `GET /health` | 200 `{"status":"online","servico":"API Meteorológica Offline"}` |
| `GET /v1/forecast?latitude=-26.4851&longitude=-49.0713` | 200, JSON com `current` (temperature_2m 24.0, relative_humidity_2m 72, apparent_temperature 24.8, precipitation 0.2, wind_speed_10m 10.5, time 2026-11-12T09:00) e `current_units` |
| `GET /v1/forecast?latitude=10&longitude=10` | 404 "Localidade não encontrada." |
| `GET /v1/forecast?...&current=temperature` | 400 "Variável atual não disponível: temperature" |

## Verificação de endpoint, parâmetros e campos
Endpoint, nomes dos parâmetros e chaves conferidos com a documentação (Anexo 2). Sem endereços externos.

## Testes da aplicação
| Teste | Resultado |
|---|---|
| `python -m py_compile consumidor_api.py frontend.py` | OK |
| `python consumidor_api.py` (API ligada) | Dicionário com os 6 campos e as unidades |
| Interface Streamlit (API ligada) | 6 indicadores corretos, sem exceções |
| Consumidor com API desligada | `ErroConsulta`: mensagem de falha de conexão |
| Interface com API desligada | `st.error` com a mensagem; nenhum dado exibido, sem travar |

## Falhas encontradas e correções
- Ao desligar a API, o consumidor lançava `ConnectionError` do requests → tratado com `try/except` e `ErroConsulta`, com mensagem orientando verificar o Uvicorn.
- `pandas` não é usado pela aplicação → não incluído no `requirements.txt`.
