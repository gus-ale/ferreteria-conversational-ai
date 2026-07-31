import httpx

from app.core.config import Settings
from app.core.errors import ProviderUnavailableError
from app.core.security import privacy_preserving_user_id
from app.services.tools import tool_definitions


class RealtimeService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def create_client_secret(self, user_id: str) -> dict:
        if not self.settings.realtime_enabled:
            raise ProviderUnavailableError(
                "La voz Realtime está desactivada. Configure REALTIME_ENABLED=true."
            )
        if self.settings.openai_api_key is None:
            raise ProviderUnavailableError("OpenAI no está configurado")

        headers = {
            "Authorization": (f"Bearer {self.settings.openai_api_key.get_secret_value()}"),
            "Content-Type": "application/json",
            "OpenAI-Safety-Identifier": privacy_preserving_user_id(user_id),
        }
        payload = {
            "session": {
                "type": "realtime",
                "model": self.settings.openai_realtime_model,
                "instructions": (
                    "Sos FerreBot, asistente de una ferretería argentina. "
                    "Respondé en español claro. Nunca inventes precios, stock, "
                    "garantías ni especificaciones. Usá las herramientas del "
                    "backend y ofrecé derivación humana cuando corresponda."
                ),
                "audio": {
                    "output": {
                        "voice": self.settings.openai_realtime_voice,
                    }
                },
                "tools": [
                    {key: value for key, value in definition.items() if key != "strict"}
                    for definition in tool_definitions()
                ],
                "tool_choice": "auto",
            }
        }

        try:
            async with httpx.AsyncClient(timeout=self.settings.openai_timeout_seconds) as client:
                response = await client.post(
                    "https://api.openai.com/v1/realtime/client_secrets",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                return response.json()
        except (httpx.TimeoutException, httpx.NetworkError) as exc:
            raise ProviderUnavailableError("No se pudo conectar con OpenAI Realtime") from exc
        except httpx.HTTPStatusError as exc:
            raise ProviderUnavailableError(
                f"OpenAI Realtime respondió con estado {exc.response.status_code}"
            ) from exc
