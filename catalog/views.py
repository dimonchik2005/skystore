from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from catalog.forms import ProductForm
from catalog.models import Product


def home(request):
    """Отображает главную страницу со списком товаров."""
    products = Product.objects.all()

    paginator = Paginator(products, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "page_obj": page_obj,
    }

    return render(request, "catalog/home.html", context)


def product_detail(request, pk):
    """Отображает подробную информацию о товаре."""
    product = get_object_or_404(Product, pk=pk)

    context = {
        "product": product,
    }

    return render(request, "catalog/product_detail.html", context)


def product_create(request):
    """Создаёт новый товар через форму."""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save()

            messages.success(
                request,
                "Товар успешно добавлен.",
            )

            return redirect(
                "product_detail",
                pk=product.pk,
            )
    else:
        form = ProductForm()

    context = {
        "form": form,
    }

    return render(request, "catalog/product_form.html", context)


def contacts(request):
    """Отображает страницу контактов и обрабатывает форму."""
    if request.method == "POST":
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

    return render(request, "catalog/contacts.html")
