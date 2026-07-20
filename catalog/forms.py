from django import forms

from catalog.models import Product


class ProductForm(forms.ModelForm):
    """Форма создания нового товара."""

    description = forms.CharField(
        required=True,
        label="Описание",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Введите описание товара",
            }
        ),
    )
    image = forms.ImageField(
        required=True,
        label="Изображение",
        widget=forms.ClearableFileInput(
            attrs={"class": "form-control"}
        ),
    )

    class Meta:
        model = Product
        fields = (
            "name",
            "description",
            "image",
            "category",
            "price",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите название товара",
                }
            ),
            "category": forms.Select(
                attrs={"class": "form-select"}
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                    "placeholder": "Введите цену",
                }
            ),
        }