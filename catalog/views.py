from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from catalog.forms import ProductForm
from catalog.models import Product


class ProductListView(ListView):
    """Отображает список продуктов."""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.all()


class ProductDetailView(DetailView):
    """Отображает один продукт."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    """Создаёт новый продукт."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)

        messages.success(
            self.request,
            "Продукт успешно создан.",
        )

        return response

    def get_success_url(self):
        return reverse(
            "product_detail",
            kwargs={"pk": self.object.pk},
        )


class ProductUpdateView(UpdateView):
    """Редактирует существующий продукт."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)

        messages.success(
            self.request,
            "Продукт успешно обновлён.",
        )

        return response

    def get_success_url(self):
        return reverse(
            "product_detail",
            kwargs={"pk": self.object.pk},
        )


class ProductDeleteView(DeleteView):
    """Удаляет продукт."""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Продукт успешно удалён.",
        )

        return super().form_valid(form)


class ContactsView(View):
    """Отображает контакты и обрабатывает форму."""

    template_name = "catalog/contacts.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        print("Получена форма обратной связи:")
        print(f"Имя: {name}")
        print(f"Телефон: {phone}")
        print(f"Сообщение: {message}")

        messages.success(
            request,
            "Сообщение успешно отправлено!",
        )

        return redirect("contacts")