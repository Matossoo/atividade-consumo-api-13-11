# Explicação técnica

## Funções dos principais comandos
**consumidor_api.py**
- `import requests`: biblioteca para fazer requisições HTTP.
- `URL_API`, `LATITUDE`, `LONGITUDE`: endpoint local e coordenadas de Jaraguá do Sul definidos na atividade.
- `parametros = {...}`: parâmetros obrigatórios da consulta (`latitude` e `longitude`).
- `requests.get(URL_API, params=parametros, timeout=10)`: envia o GET à API; `timeout` evita espera infinita.
- `resposta.raise_for_status()`: gera exceção se o status HTTP for de erro (400, 404, 500).
- `resposta.json()`: converte o corpo JSON em dicionário Python.
- `dados["current"]` / `dados["current_units"]`: acessam os valores atuais e suas unidades.
- `try / except`: transformam falhas de conexão, tempo esgotado, erro HTTP, JSON inválido e campo ausente em `ErroConsulta`, com mensagem clara.
- `return {...}`: devolve só os campos necessários (temperatura, umidade_relativa, sensacao_termica, precipitacao, velocidade_vento, horario) e as unidades.

**frontend.py**
- `import streamlit as st` e `from consumidor_api import ...`: usa o consumidor, sem fazer outra requisição.
- `st.set_page_config`, `st.title`, `st.caption`: configuração, título e localidade.
- `st.button` + `st.rerun()`: atualiza os dados.
- `st.spinner`: indica consulta em andamento; `st.success`: consulta concluída.
- `st.columns` + `st.metric`: exibem cada indicador com rótulo, valor e unidade.
- `datetime.fromisoformat(...).strftime(...)`: formata o horário da API (ISO 8601) para dd/mm/aaaa hh:mm.
- `except ErroConsulta` → `st.error`: mostra a falha separada dos dados meteorológicos.

## Fluxo dos dados
1. O Streamlit executa `frontend.py` e chama `obter_dados_meteorologicos()`.
2. O consumidor monta os parâmetros (latitude e longitude).
3. O consumidor envia GET para `http://127.0.0.1:8000/v1/forecast`.
4. A API (FastAPI) lê o JSON local e responde.
5. O consumidor verifica o status HTTP com `raise_for_status()`.
6. O corpo é convertido com `.json()`.
7. São selecionados os campos de `current` e as unidades de `current_units`.
8. O consumidor retorna um dicionário à interface.
9. A interface exibe cada valor com `st.metric`; se houver falha, exibe `st.error`.

## Análise de melhorias
- Adicionar dados horários (`hourly`) e um gráfico.
- Guardar a consulta em cache para reduzir requisições.
- Permitir escolher outras localidades (hoje a base só tem Jaraguá do Sul).
- Criar testes automatizados do consumidor.
