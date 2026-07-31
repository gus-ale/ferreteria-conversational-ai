# Voz con Realtime

## Configuración

La voz está desactivada por defecto para evitar consumo accidental.

```env
REALTIME_ENABLED=true
OPENAI_API_KEY=...
OPENAI_REALTIME_MODEL=gpt-realtime-2.1
OPENAI_REALTIME_VOICE=marin
```

La API key normal nunca se incluye en JavaScript. FastAPI solicita un secreto
temporal a `/v1/realtime/client_secrets` y el navegador lo utiliza para
establecer WebRTC.

## Eventos principales

| Evento | Dirección | Uso |
|---|---|---|
| `response.done` | OpenAI → navegador | Respuesta completa o function call |
| `conversation.item.create` | Navegador → OpenAI | Entrega un resultado de herramienta |
| `response.create` | Navegador → OpenAI | Pide continuar después de la herramienta |
| `input_audio_buffer.speech_started` | OpenAI → navegador | VAD detectó voz |

## Herramientas

Las herramientas de Realtime son las mismas que en texto:

- `search_products`
- `get_stock`
- `search_knowledge`
- `request_handoff`

El endpoint `/api/v1/realtime/tool` aplica la misma allowlist y los mismos
modelos Pydantic. El cliente nunca recibe credenciales de MySQL.

## Producción

Antes de publicar:

- exigir autenticación para crear tokens y ejecutar herramientas;
- aplicar rate limiting por usuario;
- reemplazar el identificador anónimo por un identificador interno estable;
- registrar consentimiento de audio;
- definir retención y borrado;
- revisar costos y duración de sesiones;
- usar HTTPS;
- considerar controles server-side complementarios.

