class DomainError(Exception):
    status_code = 400
    code = "domain_error"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NotFoundError(DomainError):
    status_code = 404
    code = "not_found"


class GuardrailBlockedError(DomainError):
    status_code = 400
    code = "guardrail_blocked"


class ConversationClosedError(DomainError):
    status_code = 409
    code = "conversation_closed"


class ProviderUnavailableError(DomainError):
    status_code = 503
    code = "provider_unavailable"


class AgentTurnLimitError(DomainError):
    status_code = 503
    code = "agent_turn_limit"
