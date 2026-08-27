from django.conf import settings
from django.core.cache import cache

from catalog.models import Product


def get_products_by_category(category_id: int) -> list[Product]:
    """Возвращает продукты категории с использованием кеша."""

    cache_key = f"category_{category_id}"

    if settings.CACHE_ENABLED:
        cached_products = cache.get(cache_key)

        if cached_products is not None:
            return cached_products

    products = list(
        Product.objects.filter(
            category_id=category_id,
        ).select_related("category")
    )

    if settings.CACHE_ENABLED:
        cache.set(
            cache_key,
            products,
            settings.CACHE_TTL,
        )

    return products