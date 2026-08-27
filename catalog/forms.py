from django import forms

from catalog.models import Product


FORBIDDEN_WORDS = (
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "обман",
    "полиция",
)

ALLOWED_IMAGE_TYPES = (
    "image/jpeg",
    "image/png",
)

MAX_IMAGE_SIZE = 5 * 1024 * 1024


class ProductForm(forms.ModelForm):
    """Форма создания и редактирования продукта."""

    class Meta:
        model = Product
        fields = (
            "name",
            "description",
            "image",
            "category",
            "price",
            "is_published"
        )

    def __init__(self, *args, **kwargs):
        """Добавляет Bootstrap-стили ко всем полям."""
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            widget = field.widget

            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"

            elif isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"

            else:
                widget.attrs["class"] = "form-control"

            if not isinstance(
                widget,
                (
                    forms.CheckboxInput,
                    forms.ClearableFileInput,
                    forms.Select,
                ),
            ):
                widget.attrs.setdefault(
                    "placeholder",
                    field.label,
                )

        self.fields["description"].widget.attrs.update(
            {
                "rows": 5,
                "placeholder": "Введите описание продукта",
            }
        )

    @staticmethod
    def validate_forbidden_words(
        value: str,
        field_name: str,
    ) -> str:
        """Проверяет текст на наличие запрещённых слов."""
        normalized_value = value.casefold()

        for forbidden_word in FORBIDDEN_WORDS:
            if forbidden_word in normalized_value:
                raise forms.ValidationError(
                    f'Поле «{field_name}» содержит запрещённое '
                    f'слово: «{forbidden_word}».'
                )

        return value

    def clean_name(self) -> str:
        """Проверяет название продукта."""
        name = self.cleaned_data["name"]

        return self.validate_forbidden_words(
            name,
            "Название",
        )

    def clean_description(self) -> str:
        """Проверяет описание продукта."""
        description = self.cleaned_data["description"]

        return self.validate_forbidden_words(
            description,
            "Описание",
        )

    def clean_price(self):
        """Запрещает отрицательную цену."""
        price = self.cleaned_data.get("price")

        if price is not None and price < 0:
            raise forms.ValidationError(
                "Цена продукта не может быть отрицательной."
            )

        return price

    def clean_image(self):
        """Проверяет формат и размер нового изображения."""
        image = self.cleaned_data.get("image")

        if image is None:
            return image

        content_type = getattr(image, "content_type", None)

        if (
            content_type is not None
            and content_type not in ALLOWED_IMAGE_TYPES
        ):
            raise forms.ValidationError(
                "Разрешены только изображения JPEG и PNG."
            )

        image_size = getattr(image, "size", 0)

        if image_size > MAX_IMAGE_SIZE:
            raise forms.ValidationError(
                "Размер изображения не должен превышать 5 МБ."
            )

        return image