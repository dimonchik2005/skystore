from django.contrib import messages
from django.shortcuts import redirect, render


def home(request):
    """Отображает главную страницу магазина."""
    return render(request, "catalog/home.html")


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

        messages.success(request, "Сообщение успешно отправлено!")
        return redirect("contacts")

    return render(request, "catalog/contacts.html")
