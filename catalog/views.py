from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from catalog.forms import ProductForm
from catalog.models import Product


class ProductUnpublishView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    View,
):
    permission_required = (
        "catalog.can_unpublish_product"
    )
    raise_exception = True

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save(update_fields=["is_published"])

        messages.success(
            request,
            "Публикация продукта отменена.",
        )

        return redirect(
            "catalog:product_detail",
            pk=product.pk,
        )


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Отображает один продукт."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создаёт новый продукт."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields.pop("is_published", None)

        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "catalog:product_detail",
            kwargs={"pk": self.object.pk},
        )


class ProductUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView,
):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    raise_exception = True

    def test_func(self):
        product = self.get_object()
        user = self.request.user

        return (
                product.owner_id == user.id
                or user.has_perm(
            "catalog.can_unpublish_product"
        )
        )

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if not self.request.user.has_perm(
                "catalog.can_unpublish_product"
        ):
            form.fields.pop("is_published", None)

        return form

    def get_success_url(self):
        return reverse_lazy(
            "catalog:product_detail",
            kwargs={"pk": self.object.pk},
        )


class ProductDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView,
):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:product_list")
    raise_exception = True

    def test_func(self):
        product = self.get_object()
        user = self.request.user

        return (
                product.owner_id == user.id
                or user.has_perm("catalog.delete_product")
        )


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


class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.all()
