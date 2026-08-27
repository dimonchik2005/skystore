from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """Настройки блоговых записей в админке."""

    list_display = (
        "id",
        "title",
        "is_published",
        "views_count",
        "created_at",
    )
    list_filter = (
        "is_published",
        "created_at",
    )
    search_fields = (
        "title",
        "content",
    )
