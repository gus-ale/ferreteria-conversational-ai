import re
from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.knowledge import KnowledgeDocument


@dataclass(frozen=True)
class KnowledgeMatch:
    title: str
    source: str
    content: str
    score: float


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[\wáéíóúüñ-]{3,}", text.lower()))


async def search_knowledge(
    session: AsyncSession,
    query: str,
    *,
    top_k: int,
) -> list[KnowledgeMatch]:
    documents = list((await session.scalars(select(KnowledgeDocument))).all())
    query_tokens = tokenize(query)
    matches: list[KnowledgeMatch] = []

    for document in documents:
        document_tokens = tokenize(f"{document.title} {document.content}")
        if not query_tokens:
            continue
        overlap = len(query_tokens & document_tokens)
        score = overlap / len(query_tokens)
        if score > 0:
            matches.append(
                KnowledgeMatch(
                    title=document.title,
                    source=document.source,
                    content=document.content,
                    score=round(score, 4),
                )
            )

    return sorted(matches, key=lambda item: item.score, reverse=True)[:top_k]


async def seed_knowledge(session: AsyncSession) -> None:
    if await session.scalar(select(func.count(KnowledgeDocument.id))):
        return

    session.add_all(
        [
            KnowledgeDocument(
                title="Manual del taladro percutor T700",
                source="demo/manual-taladro-t700",
                content=(
                    "El taladro T700 posee 700 W, mandril de 13 mm y modo "
                    "percutor. Para mampostería se utiliza una mecha apta para "
                    "hormigón. Debe desconectarse antes de cambiar la mecha."
                ),
            ),
            KnowledgeDocument(
                title="Política de garantía",
                source="demo/politica-garantia",
                content=(
                    "La garantía comercial de demostración es de 12 meses para "
                    "defectos de fabricación. No cubre desgaste, humedad, golpes "
                    "ni uso contrario al manual."
                ),
            ),
            KnowledgeDocument(
                title="Cambios y devoluciones",
                source="demo/cambios-devoluciones",
                content=(
                    "Los cambios requieren comprobante de compra y producto sin "
                    "uso dentro de los 30 días. Los productos eléctricos abiertos "
                    "se revisan técnicamente antes de aceptar una devolución."
                ),
            ),
        ]
    )
    await session.commit()
