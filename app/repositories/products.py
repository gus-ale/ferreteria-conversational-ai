import re

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def search_products(
    session: AsyncSession,
    query: str,
    *,
    limit: int = 5,
) -> list[Product]:
    terms = re.findall(r"[\wáéíóúüñ-]+", query.lower())[:8]
    if not terms:
        return []

    conditions = []
    for term in terms:
        pattern = f"%{term}%"
        conditions.append(
            or_(
                func.lower(Product.name).like(pattern),
                func.lower(Product.description).like(pattern),
                func.lower(Product.category).like(pattern),
                func.lower(Product.sku).like(pattern),
            )
        )

    statement = (
        select(Product)
        .where(Product.active.is_(True), and_(*conditions))
        .order_by(Product.name.asc())
        .limit(limit)
    )
    result = await session.scalars(statement)
    return list(result.all())


async def seed_products(session: AsyncSession) -> None:
    if await session.scalar(select(func.count(Product.id))):
        return

    session.add_all(
        [
            Product(
                sku="MAR-M20",
                name="Martillo carpintero M20",
                description="Martillo de acero forjado con mango antideslizante.",
                category="Herramientas manuales",
                price=18500,
                stock=18,
            ),
            Product(
                sku="TAL-T700",
                name="Taladro percutor T700",
                description="Taladro percutor de 700 W con mandril de 13 mm.",
                category="Herramientas eléctricas",
                price=98500,
                stock=6,
            ),
            Product(
                sku="PIN-EXT20",
                name="Pintura exterior 20 L",
                description="Pintura acrílica lavable para paredes exteriores.",
                category="Pinturas",
                price=74200,
                stock=9,
            ),
            Product(
                sku="TOR-6X40",
                name="Tornillo 6 x 40 mm",
                description="Tornillo zincado para madera. Caja de 100 unidades.",
                category="Fijaciones",
                price=8900,
                stock=45,
            ),
        ]
    )
    await session.commit()
