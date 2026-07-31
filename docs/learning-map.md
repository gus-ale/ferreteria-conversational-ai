# Mapa de aprendizaje

| Archivo | Concepto que demuestra |
|---|---|
| `app/services/intents.py` | Intenciones y extracción de entidades |
| `app/services/agent.py` | Memoria, contexto, flujo demo y Responses API |
| `app/services/tools.py` | Function calling, JSON Schema y allowlist |
| `app/services/guardrails.py` | Inyección, secretos y sanitización |
| `app/services/realtime.py` | Token temporal y configuración de voz |
| `app/api/routes/workflows.py` | Handoff y feedback |
| `app/models/conversation.py` | Estado y persistencia conversacional |
| `app/static/app.js` | Chat web, WebRTC y eventos Realtime |
| `evals/` | Evaluación de intenciones y seguridad |
| `tests/` | Verificación automática del comportamiento |
| `alembic/` | Versionado del esquema SQL |
| `.github/workflows/ci.yml` | Integración continua |

## Orden sugerido de estudio

1. Ejecutar en modo demo.
2. Probar Swagger.
3. Leer las intenciones.
4. Seguir un mensaje por `AgentService`.
5. Revisar las herramientas.
6. Inspeccionar las tablas.
7. Ejecutar tests y evals.
8. Activar OpenAI para texto.
9. Activar Realtime para voz.
10. Reemplazar SQLite por MySQL mediante Docker.

