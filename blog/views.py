from django.db.models import F
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.models import Blog


class BlogListView(ListView):
    """Показывает список опубликованных статей."""

    model = Blog
    template_name = "blog/blog_list.html"
    context_object_name = "blogs"

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    """Показывает статью и увеличивает счётчик просмотров."""

    model = Blog
    template_name = "blog/blog_detail.html"
    context_object_name = "blog"

    def get_object(self, queryset=None):
        blog = super().get_object(queryset)

        Blog.objects.filter(pk=blog.pk).update(
            views_count=F("views_count") + 1
        )

        blog.refresh_from_db(
            fields=("views_count",)
        )

        return blog


class BlogCreateView(CreateView):
    """Создаёт новую статью."""

    model = Blog
    template_name = "blog/blog_form.html"
    fields = (
        "title",
        "content",
        "preview",
        "is_published",
    )


class BlogUpdateView(UpdateView):
    """Редактирует существующую статью."""

    model = Blog
    template_name = "blog/blog_form.html"
    fields = (
        "title",
        "content",
        "preview",
        "is_published",
    )

    def get_success_url(self):
        """Возвращает адрес отредактированной статьи."""
        return reverse(
            "blog:blog_detail",
            kwargs={"pk": self.object.pk},
        )


class BlogDeleteView(DeleteView):
    """Удаляет статью."""

    model = Blog
    template_name = "blog/blog_confirm_delete.html"
    success_url = reverse_lazy("blog:blog_list")
