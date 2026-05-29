from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Tour, Review, HeaderSettings, Booking
from .forms import ReviewForm, BookingForm
from django.contrib import messages


def get_filtered_tours(request):
    """Вспомогательная функция фильтрации для главной и каталога"""
    tours = Tour.objects.all().order_by('-tour_id')

    destination = request.GET.get('destination', '').strip()
    check_in = request.GET.get('check_in', '').strip()
    check_out = request.GET.get('check_out', '').strip()
    cost_for_one_person = request.GET.get('cost_for_one_person', '').strip()

    # ИСПРАВЛЕНО: Теперь фильтруем по полю country (страна), а не по name (название тура)
    if destination:
        tours = tours.filter(country__icontains=destination)

    if check_in:
        tours = tours.filter(date_start__gte=check_in)

    if check_out:
        tours = tours.filter(date_end__lte=check_out)

    if cost_for_one_person:
        tours = tours.filter(cost_for_one_person=cost_for_one_person)

    filters = {
        'destination': destination,
        'check_in': check_in,
        'check_out': check_out,
        'cost_for_one_person': cost_for_one_person,
    }

    return tours, filters


def index(request):
    tours, filters = get_filtered_tours(request)
    is_searched = bool(request.GET.get('destination') or request.GET.get('check_in') or request.GET.get('check_out'))
    total_found = tours.count()
    tours = tours[:3]
    has_more = total_found > 3

    return render(request, 'index.html', {
        'tours': tours,
        'filters': filters,
        'is_searched': is_searched,
        'has_more': has_more
    })


def catalog_view(request):
    """Страница каталога: выводит ВСЕ отфильтрованные туры"""
    header_settings = HeaderSettings.objects.first()
    tours, filters = get_filtered_tours(request)

    return render(request, 'catalog.html', {
        'tours': tours,
        'header_settings': header_settings,
        'filters': filters
    })


def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    reviews = Review.objects.filter(tour=tour).order_by('-created_at')
    form = ReviewForm()

    # Проверяем, забронировал ли текущий пользователь этот тур
    user_has_booked = False
    if request.user.is_authenticated:
        user_has_booked = Booking.objects.filter(user=request.user, tour=tour).exists()

    # Находим до 3-х других туров в этой же стране, исключая текущий
    similar_tours = Tour.objects.filter(country=tour.country).exclude(pk=tour.pk)[:3]

    if similar_tours.count() < 3:
        additional_tours = Tour.objects.exclude(pk=tour.pk).exclude(country=tour.country)[:3 - similar_tours.count()]
        similar_tours = list(similar_tours) + list(additional_tours)

    return render(request, 'tour_detail.html', {
        'tour': tour,
        'reviews': reviews,
        'form': form,
        'similar_tours': similar_tours,
        'user_has_booked': user_has_booked
    })


@login_required
def add_review(request, pk):
    tour = get_object_or_404(Tour, pk=pk)

    # БЭКЕНД-ЗАЩИТА: Проверяем факт покупки перед сохранением отзыва
    has_booked = Booking.objects.filter(user=request.user, tour=tour).exists()
    if not has_booked:
        messages.error(request, "Вы не можете оставить отзыв, так как не бронировали этот тур.")
        return redirect('tour_detail', pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.tour = tour
            review.user = request.user
            review.save()
            messages.success(request, "Ваш отзыв успешно добавлен!")
    return redirect('tour_detail', pk=pk)


@login_required
def book_tour(request, tour_id):
    """Представление бронирования с полной валидацией данных через Django Forms"""
    tour = get_object_or_404(Tour, pk=tour_id)
    header_settings = HeaderSettings.objects.first()

    if request.method == 'POST':
        form = BookingForm(request.POST)

        if tour.slots_left <= 0 or tour.is_expired:
            messages.error(request, "К сожалению, этот тур уже недоступен для бронирования.")
            # ИСПРАВЛЕНО: заменили несуществующий pk на tour_id, чтобы не падала ошибка NameError
            return redirect('tour_detail', pk=tour_id)

        # 1. Первая стадия: Валидация типов данных (числа, заполненность полей карты)
        if form.is_valid():
            people_count = form.cleaned_data['people_count']
            user_comment = form.cleaned_data['user_comment']

            # Подсчёт лимитов мест в БД
            current_booked = tour.booked_slots if tour.booked_slots is not None else 0
            current_total = tour.total_slots if tour.total_slots is not None else 20
            available_slots = current_total - current_booked

            # 2. Вторая стадия: Бизнес-валидация доступности мест в туре
            if available_slots >= people_count:
                # Всё отлично, создаем бронь
                Booking.objects.create(
                    user=request.user,
                    tour=tour,
                    people_count=people_count,
                    user_comment=user_comment
                )

                # Обновляем счётчик
                tour.booked_slots = current_booked + people_count
                tour.save()

                messages.success(request, f"Тур '{tour.name}' успешно забронирован!")
                return redirect('profile')
            else:
                # Ошибка лимита мест добавляется прямо в ошибки формы
                form.add_error('people_count', f"Недостаточно мест. Доступно всего: {available_slots}")
    else:
        form = BookingForm()

    # Если форма невалидна или мест не хватило, возвращаем пользователя на ту же страницу с формой, содержащей ошибки
    return render(request, 'booking.html', {
        'tour': tour,
        'header_settings': header_settings,
        'form': form
    })


@login_required
def profile_view(request):
    user_bookings = Booking.objects.filter(user=request.user).select_related('tour')
    return render(request, 'profile.html', {
        'user': request.user,
        'bookings': user_bookings,
    })