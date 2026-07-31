import re
import unicodedata


def normalize(text: str) -> str:
    without_accents = "".join(
        character
        for character in unicodedata.normalize("NFD", text.lower())
        if unicodedata.category(character) != "Mn"
    )
    return re.sub(r"\s+", " ", without_accents).strip()


INTENT_KEYWORDS: list[tuple[str, tuple[str, ...]]] = [
    (
        "human_handoff",
        (
            "hablar con una persona",
            "hablar con alguien",
            "operador humano",
            "asesor humano",
            "atencion humana",
            "vendedor",
        ),
    ),
    (
        "complaint",
        (
            "reclamo",
            "queja",
            "me cobraron mal",
            "producto roto",
            "mala atencion",
            "no funciona",
        ),
    ),
    ("returns", ("devolucion", "devolver", "cambio", "cambiar producto")),
    ("warranty", ("garantia", "garantias")),
    (
        "technical_advice",
        (
            "como usar",
            "manual",
            "sirve para",
            "recomendacion",
            "seguridad",
            "ficha tecnica",
        ),
    ),
    ("stock", ("stock", "queda", "quedan", "disponible", "hay unidades")),
    ("price", ("precio", "cuesta", "valor", "sale", "cuanto cuesta")),
    ("product_search", ("busco", "necesito", "tenes", "tienen", "producto")),
    ("goodbye", ("chau", "adios", "hasta luego", "gracias, eso es todo")),
    ("greeting", ("hola", "buen dia", "buenas tardes", "buenas noches")),
]


def classify_intent(text: str) -> str:
    normalized = normalize(text)
    for intent, keywords in INTENT_KEYWORDS:
        if any(keyword in normalized for keyword in keywords):
            return intent
    return "fallback"


STOPWORDS = {
    "a",
    "al",
    "algo",
    "cuanto",
    "cuánto",
    "cuesta",
    "costo",
    "de",
    "del",
    "disponible",
    "el",
    "en",
    "es",
    "esta",
    "está",
    "hay",
    "la",
    "las",
    "los",
    "me",
    "necesito",
    "precio",
    "queda",
    "quedan",
    "stock",
    "sale",
    "tenes",
    "tiene",
    "tienen",
    "un",
    "una",
    "valor",
    "y",
}


def extract_product_query(text: str) -> str:
    tokens = re.findall(r"[\wáéíóúüñ-]+", text.lower())
    useful = [token for token in tokens if token not in STOPWORDS]
    return " ".join(useful).strip()
