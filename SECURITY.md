# Seguridad

## Principios aplicados

- La API key de OpenAI permanece exclusivamente en FastAPI.
- El navegador recibe solamente un secreto temporal de Realtime.
- Las herramientas se validan en el backend mediante Pydantic y una allowlist.
- No existe una herramienta de SQL libre ni una función para modificar stock.
- Los documentos recuperados se tratan como datos, nunca como instrucciones.
- Las salidas se revisan para redactar patrones de secretos.
- Las conversaciones admiten derivación humana.

## Antes de producción

Este repositorio es educativo y utiliza una identidad anónima de demostración.
Antes de un despliegue comercial deben agregarse:

- autenticación real y autorización por usuario;
- rate limiting distribuido;
- gestor de secretos;
- cifrado y política de retención de conversaciones;
- consentimiento informado para audio y transcripciones;
- auditoría de accesos;
- revisión legal y de privacidad;
- herramientas Realtime ejecutadas por una conexión de servidor complementaria
  si se requiere eliminar por completo la coordinación del navegador.

## Informar vulnerabilidades

No publique credenciales ni datos personales en un issue. Describa el problema
sin incluir secretos y contacte privadamente al responsable del repositorio.

