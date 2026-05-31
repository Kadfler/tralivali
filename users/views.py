from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail  # Импортируем функцию для отправки почты
from django.conf import settings  # Импортируем настройки проекта (settings.py)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            # ================= ОТПРАВКА ПИСЬМА ПРИ РЕГИСТРАЦИИ =================
            if user.email:
                subject = "Добро пожаловать в Tralley-Valley! ✈️"
                message = (
                    f"Добро пожаловать, {user.username}!\n\n"
                    f"Вы успешно зарегистрировались в туристическом агентстве Tralley-Valley.\n"
                    f"Теперь вам доступно быстрое бронирование туров, управление заказами "
                    f"и история ваших путешествий прямо в личном кабинете.\n\n"
                    f"Откройте мир вместе с нами!\n\n"
                    f"С уважением, команда Tralley-Valley"
                )
                try:
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=True,  # Сайт не упадет, если у почтового сервера будут проблемы
                    )
                except Exception:
                    pass
            # ===================================================================

            login(request, user)
            return redirect('catalog')

    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {
        'form': form
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('catalog')

    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {
        'form': form
    })
