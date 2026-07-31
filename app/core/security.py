import hashlib
import hmac

from fastapi import Header

from app.core.config import settings
from app.core.errors import DomainError


class UnauthorizedError(DomainError):
    status_code = 401
    code = "unauthorized"


async def require_admin_key(
    x_admin_key: str | None = Header(default=None, alias="X-Admin-Key"),
) -> None:
    expected = settings.admin_api_key.get_secret_value()
    if x_admin_key is None or not hmac.compare_digest(x_admin_key, expected):
        raise UnauthorizedError("A valid X-Admin-Key header is required")


def privacy_preserving_user_id(user_id: str) -> str:
    normalized = user_id.strip().lower().encode("utf-8")
    return hashlib.sha256(normalized).hexdigest()
