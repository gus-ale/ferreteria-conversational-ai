# Ejemplos de API

## Chat

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"¿Cuánto stock queda del martillo M20?"}'
```

## Continuar una conversación

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message":"¿Y cuánto cuesta?",
    "conversation_id":"ID_DEVUELTO_POR_EL_PRIMER_MENSAJE"
  }'
```

## Feedback

```bash
curl -X POST http://localhost:8000/api/v1/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id":"ID_DE_CONVERSACION",
    "rating":5,
    "comment":"Respuesta clara"
  }'
```

## Solicitar una sesión de voz

```bash
curl -X POST http://localhost:8000/api/v1/realtime/token \
  -H "Content-Type: application/json" \
  -d '{"user_id":"usuario-interno-123"}'
```

Este último ejemplo requiere `REALTIME_ENABLED=true` y `OPENAI_API_KEY`.

