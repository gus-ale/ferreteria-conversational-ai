# Ferretería Conversational AI

[![CI](https://github.com/gus-ale/ferreteria-conversational-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/gus-ale/ferreteria-conversational-ai/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-Responses_%2B_Realtime-412991.svg)](https://developers.openai.com/api/docs/guides/realtime)
[![License MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Asistente conversacional multimodal para una ferretería, desarrollado como
proyecto profesional de portfolio. Combina FastAPI, diseño conversacional,
memoria, function calling, recuperación documental, derivación humana,
evaluaciones, MySQL, Docker y voz mediante OpenAI Realtime.

> Los productos, precios, stock, políticas y documentos son sintéticos. El
> proyecto es educativo y no representa información comercial real.

## Qué demuestra

Este repositorio se concentra en el trabajo de un **Conversational AI /
Chatbot Developer**:

- identificación de intenciones;
- continuidad de contexto;
- estados de conversación;
- respuestas de fallback;
- derivación a una persona;
- feedback del usuario;
- herramientas controladas;
- texto mediante Responses API;
- voz mediante Realtime y WebRTC;
- seguridad, pruebas y evaluaciones.

No es una copia de `ferreteria-generative-ai`. Aquel proyecto profundiza el
pipeline generativo y RAG; este profundiza la experiencia conversacional,
canales, estados, handoff y voz.

## Demostración web

La aplicación incluye una interfaz responsive:

- chat por texto;
- preguntas sugeridas;
- visualización de intención y estado;
- botón para iniciar voz;
- acceso directo a Swagger.

En modo demo, el texto funciona sin credenciales ni consumo. La voz permanece
desactivada hasta configurar una API key.

## Capacidades

### Conversación

- Intenciones: saludo, búsqueda, precio, stock, garantía, devolución,
  asesoramiento técnico, reclamo, derivación y despedida.
- Memoria persistida en SQL.
- Reutilización del producto mencionado en una pregunta anterior.
- Estados `active`, `waiting_human` y `closed`.
- Historial consultable para auditoría.

### Herramientas

- `search_products`
- `get_stock`
- `search_knowledge`
- `request_handoff`

El modelo propone llamadas, pero FastAPI:

1. verifica que la herramienta esté permitida;
2. valida los argumentos con Pydantic;
3. ejecuta código controlado;
4. consulta SQL;
5. devuelve un resultado estructurado.

No existe una herramienta de SQL libre ni una función para modificar stock,
precios o pedidos.

### Voz

- Token temporal generado por FastAPI.
- API key mantenida en el servidor.
- WebRTC para micrófono y audio.
- VAD e interrupciones administradas por Realtime.
- Function calls detectadas mediante eventos.
- Herramientas de voz validadas por el backend.
- Identificador de seguridad derivado mediante SHA-256.

La implementación sigue las guías oficiales de
[WebRTC](https://developers.openai.com/api/docs/guides/realtime-webrtc) y
[conversaciones Realtime](https://developers.openai.com/api/docs/guides/realtime-conversations).

### Calidad

- Guardrails de entrada y salida.
- Allowlist de herramientas.
- Evaluaciones determinísticas.
- Tests de API y workflows.
- Liveness y readiness.
- Métricas Prometheus.
- IDs de petición.
- Migraciones Alembic.
- CI con GitHub Actions.
- Docker y MySQL.

## Arquitectura

```mermaid
flowchart TD
    U["Usuario"] --> UI["Chat y voz"]
    UI --> API["FastAPI"]
    API --> G["Guardrails e intenciones"]
    G --> A["Orquestador"]
    A --> O["Responses y Realtime"]
    A --> T["Herramientas"]
    T --> DB[("Productos y memoria")]
    T --> R[("Documentación")]
    A --> H["Atención humana"]
```

Consultar [arquitectura y decisiones](docs/architecture.md).

## Inicio rápido en modo demo

Requisitos:

- Python 3.11 o superior;
- Git;
- Windows con WSL2, Linux o macOS.

En WSL:

```bash
cd ferreteria-conversational-ai
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Abrir:

| Recurso | Dirección |
|---|---|
| Aplicación | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Readiness | http://localhost:8000/api/v1/health/ready |
| Métricas | http://localhost:8000/metrics |

El modo demo carga cuatro productos y tres documentos sintéticos.

## Consultas para probar

```text
Hola, buen día
¿Cuánto stock queda del martillo M20?
¿Y cuánto cuesta?
¿Qué garantía tiene el taladro T700?
¿Cómo uso el modo percutor?
Quiero hablar con una persona
```

La segunda pregunta breve demuestra memoria contextual: FerreBot reutiliza el
producto mencionado en el turno anterior.

## Activar OpenAI para texto

Editar `.env`:

```env
AI_PROVIDER=openai
OPENAI_API_KEY=tu_clave
OPENAI_TEXT_MODEL=gpt-5.6-sol
```

El modelo se configura mediante variables de entorno para poder evaluarlo y
cambiarlo sin editar el código. El agente utiliza Responses API y devuelve
resultados de herramientas mediante `function_call_output`, siguiendo el flujo
descrito en la guía oficial de
[function calling](https://developers.openai.com/api/docs/guides/function-calling).

## Activar voz

Editar `.env`:

```env
REALTIME_ENABLED=true
OPENAI_API_KEY=tu_clave
OPENAI_REALTIME_MODEL=gpt-realtime-2.1
OPENAI_REALTIME_VOICE=marin
```

Reiniciar la aplicación y pulsar **Voz**.

Flujo:

1. El navegador solicita un secreto temporal.
2. FastAPI se comunica con OpenAI usando la clave privada.
3. El navegador abre WebRTC con el secreto temporal.
4. Realtime escucha y responde con audio.
5. Si necesita datos, genera una llamada a función.
6. El navegador reenvía la solicitud a FastAPI.
7. FastAPI valida y ejecuta la herramienta.
8. El resultado vuelve a Realtime y FerreBot responde con voz.

Consultar [guía de Realtime del proyecto](docs/realtime.md).

## MySQL con Docker

Copiar la configuración:

```bash
cp .env.example .env
```

`compose.yaml` sobrescribe automáticamente la conexión de la API con:

```env
DATABASE_URL=mysql+asyncmy://ferrebot:ferrebot-change-me@mysql:3306/ferreteria_conversational
```

Iniciar:

```bash
docker compose up --build
```

La API queda en `http://localhost:8000` y MySQL se publica localmente en el
puerto `3307`.

Las contraseñas incluidas son únicamente de desarrollo y deben reemplazarse.

## Endpoints

| Método | Endpoint | Uso |
|---|---|---|
| `GET` | `/api/v1/health/live` | Proceso vivo |
| `GET` | `/api/v1/health/ready` | Dependencias preparadas |
| `POST` | `/api/v1/chat` | Mensaje de texto |
| `GET` | `/api/v1/chat/conversations/{id}` | Historial |
| `POST` | `/api/v1/handoffs` | Derivación explícita |
| `POST` | `/api/v1/feedback` | Valoración 1–5 |
| `GET` | `/api/v1/realtime/config` | Disponibilidad de voz |
| `POST` | `/api/v1/realtime/token` | Secreto temporal |
| `POST` | `/api/v1/realtime/tool` | Herramientas de voz |
| `GET` | `/metrics` | Métricas Prometheus |

Hay ejemplos en [docs/api-examples.md](docs/api-examples.md).

## Tests y evaluaciones

```bash
pytest --cov=app --cov-report=term-missing
python -m evals.run_evals
ruff check .
ruff format --check .
```

Los tests cubren:

- salud y frontend;
- clasificación de intenciones;
- consultas de stock;
- memoria contextual;
- RAG con citas;
- prompt injection;
- handoff;
- feedback;
- configuración segura de Realtime.

Las evaluaciones de `evals/cases.json` funcionan como un pequeño dataset de
regresión conversacional. Si una modificación cambia una intención o permite
una solicitud peligrosa, CI debe detectarlo.

## Seguridad y límites

- `.env` está excluido de Git.
- La API key no se envía al navegador.
- El navegador recibe un secreto Realtime temporal.
- Los argumentos de herramientas se validan.
- Las herramientas peligrosas no existen.
- Se bloquean patrones básicos de inyección y extracción de secretos.
- Las respuestas redactan formatos típicos de credenciales.
- Los documentos se consideran datos no confiables.

Este portfolio no reemplaza autenticación, rate limiting, consentimiento de
audio ni una política de privacidad comercial. Consultar [SECURITY.md](SECURITY.md).

## Mapa para estudiar el código

Consultar [docs/learning-map.md](docs/learning-map.md). El recorrido recomendado
es:

1. `app/main.py`
2. `app/api/routes/chat.py`
3. `app/services/intents.py`
4. `app/services/agent.py`
5. `app/services/tools.py`
6. `app/services/realtime.py`
7. `app/static/app.js`
8. `tests/`
9. `evals/`

## Portfolio

Este proyecto permite demostrar:

- Python asíncrono;
- FastAPI y OpenAPI;
- SQLAlchemy y MySQL;
- modelado de conversación;
- OpenAI Responses API;
- OpenAI Realtime API;
- function calling;
- RAG básico;
- seguridad de agentes;
- WebRTC;
- pruebas, evaluación y CI/CD;
- Docker y observabilidad.
