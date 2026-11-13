# Projeto Meteorológico — Jaraguá do Sul/SC

Aplicação em Python que consome a **API Meteorológica Offline** (executada localmente) e exibe os dados em uma interface web feita com **Streamlit**.

## Arquitetura
API (FastAPI, `127.0.0.1:8000`) → `consumidor_api.py` (requests + JSON) → `frontend.py` (Streamlit)

## Tecnologias
Python, requests, Streamlit, Git.

## Arquivos
| Arquivo | Finalidade |
|---|---|
| `consumidor_api.py` | Requisição HTTP à API, verificação da resposta, interpretação do JSON e tratamento de falhas |
| `frontend.py` | Interface Streamlit que exibe os dados |
| `requirements.txt` | Dependências do projeto |
| `.gitignore` | Arquivos fora do versionamento |
| `EXPLICACAO_TECNICA.md` | Lógica do código e fluxo de dados |
| `REGISTRO_TESTES.md` | Testes realizados, falhas e correções |

## Requisitos
Python 3, Git, e a API do docente em execução.

## 1. Executar a API (terminal 1, pasta separada)
```powershell
git clone https://github.com/jpsvalentim/api-meteorologica-offline.git
cd api-meteorologica-offline
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Endereço da API: `http://127.0.0.1:8000` (documentação em `/docs`). Mantenha este terminal aberto.

## 2. Executar a aplicação (terminal 2)
```powershell
cd projeto_meteorologico
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run frontend.py
```
Abra no navegador o endereço mostrado no terminal.

## Testes
1. Verificar a API: `http://127.0.0.1:8000/health`
2. Postman (GET): `http://127.0.0.1:8000/v1/forecast` com `latitude = -26.4851` e `longitude = -49.0713`; conferir status 200 e o grupo `current`.
3. Sintaxe: `python -m py_compile consumidor_api.py frontend.py`
4. Consumidor isolado: `python consumidor_api.py`
5. Aplicação completa: `python -m streamlit run frontend.py`

Detalhes em `REGISTRO_TESTES.md`.

## Limitações
Os dados são simulados (arquivo JSON local), não medições em tempo real. A API precisa estar em execução; caso contrário a interface exibe uma mensagem de erro.
