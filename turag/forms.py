from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating', 'image']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-select'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your review...'}),
        }

class BookingForm(forms.Form):
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