from django import forms
from .models import Review, AddService
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating', 'image']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-select'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your review...'}),
        }


class BookingForm(forms.Form):
    services = forms.ModelMultipleChoiceField(
        queryset=AddService.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label="Дополнительные услуги"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Этот метод переопределяет, как именно отображается каждая услуга в списке
        self.fields['services'].label_from_instance = lambda obj: f"{obj.name} (+{obj.cost} ₽)"

    people_count = forms.IntegerField(
        min_value=1,
        initial=1,
        label="Количество человек",
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg bg-light text-dark border-light-subtle',
            'min': '1'
        })
    )
    user_comment = forms.CharField(
        required=False,
        label="Комментарий к бронированию",
        widget=forms.Textarea(attrs={
            'class': 'form-control bg-light text-dark border-light-subtle',
            'rows': '3',
            'placeholder': 'Например, нужны раздельные кровати или тихий номер...'
        })
    )

    # Поля псевдо-оплаты (тоже валидируем на заполненность)
    card_number = forms.CharField(
        max_length=19,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-white text-dark border-light-subtle form-control-lg fs-6',
            'placeholder': '0000 0000 0000 0000'
        })
    )
    card_expiry = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-white text-dark border-light-subtle',
            'placeholder': 'ММ/ГГ'
        })
    )
    card_cvc = forms.CharField(
        max_length=3,
        widget=forms.PasswordInput(render_value=True, attrs={
            'class': 'form-control bg-white text-dark border-light-subtle',
            'placeholder': '***',
            'maxlength': '3'
        })
    )

    def clean_card_number(self):
        data = self.cleaned_data['card_number']
        if not re.match(r'^\d{4} \d{4} \d{4} \d{4}$', data):
            raise ValidationError("Введите номер карты в формате 0000 0000 0000 0000")
        return data

    def clean_card_expiry(self):
        data = self.cleaned_data['card_expiry']
        if not re.match(r'^(0[1-9]|1[0-2])\/\d{2}$', data):
            raise ValidationError("Введите дату в формате ММ/ГГ")
        return data

    def clean_card_cvc(self):
        data = self.cleaned_data['card_cvc']
        if not re.match(r'^\d{3}$', data):
            raise ValidationError("CVC должен состоять из 3 цифр")
        return data

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User  # Используем стандартного User
        fields = ['username', 'first_name', 'last_name', 'email']  # Убрали 'avatar'!
        labels = {
            'username': 'Никнейм',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электронная почта',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Навешиваем Bootstrap-класс на все текстовые поля формы
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})