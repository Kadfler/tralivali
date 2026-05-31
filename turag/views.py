from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Tour, Review, HeaderSettings, Booking, AddService
from .forms import ReviewForm, BookingForm, ProfileEditForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import F, DurationField, ExpressionWrapper, IntegerField, Case, When, Value
from django.core.paginator import Paginator
from django.core.mail import send_mail  # Импорт утилиты отправки почты
from django.conf import settings  # Импорт настроек проекта settings.py


def get_filtered_tours(request, tours_queryset):
    """
    Вспомогательная функция для фильтрации туров по поисковому запросу.
    """
    destination = request.GET.get('destination', '').strip()
    check_in = request.GET.get('check_in', '')
    check_out = request.GET.get('check_out', '')

    if destination:
        tours_queryset = tours_queryset.filter(country__icontains=destination)
    if check_in:
        tours_queryset = tours_queryset.filter(date_start__gte=check_in)
    if check_out:
        tours_queryset = tours_queryset.filter(date_end__lte=check_out)

    filters = {
        'destination': destination,
        'check_in': check_in,
        'check_out': check_out,
    }

    return tours_queryset, filters


def index(request):
    """
    Контроллер главной страницы с тотальной очисткой от архивов.
    """
    current_date = timezone.now().date()
    live_tours = Tour.objects.filter(
        date_end__gte=current_date,  # Не архивный
        booked_slots__lt=F('total_slots')  # Есть места
    )

    tours, filters = get_filtered_tours(request, live_tours)
    is_searched = bool(request.GET.get('destination') or request.GET.get('check_in') or request.GET.get('check_out'))

    popular_tours = Tour.objects.filter(
        date_end__gte=current_date,
        booked_slots__lt=F('total_slots')
    ).order_by('-tour_id')[:3]

    total_found = tours.count()
    tours = tours[:3]  # Ограничиваем до 3 штук на главной
    has_more = total_found > 3

    return render(request, 'index.html', {
        'tours': tours,
        'filters': filters,
        'is_searched': is_searched,
        'has_more': has_more,
        'popular_tours': popular_tours,
    })


def catalog_view(request):
    """
    Основная функция контроллера для отображения страницы каталога.
    Архивные туры видны ТОЛЬКО администраторам/персоналу.
    """
    current_date = timezone.now().date()

    # Проверяем, является ли пользователь администратором или сотрудником
    if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
        initial_queryset = Tour.objects.all()
    else:
        # Для обычных пользователей отсекаем архивные туры по дате окончания
        initial_queryset = Tour.objects.filter(date_end__gte=current_date)

    tours_queryset, filters = get_filtered_tours(request, initial_queryset)
    sort_by = request.GET.get('sort_by', 'name_asc')

    # Применяем сортировку к отфильтрованному списку
    if sort_by == 'name_asc':
        tours_queryset = tours_queryset.order_by('name')
    elif sort_by == 'name_desc':
        tours_queryset = tours_queryset.order_by('-name')
    elif sort_by == 'price_asc':
        tours_queryset = tours_queryset.order_by('cost_for_one_person')
    elif sort_by == 'price_desc':
        tours_queryset = tours_queryset.order_by('-cost_for_one_person')
    elif sort_by == 'duration_asc':
        tours_queryset = tours_queryset.annotate(
            calculated_duration=ExpressionWrapper(
                F('date_end') - F('date_start'),
                output_field=DurationField()
            )
        ).order_by('calculated_duration')
    elif sort_by == 'duration_desc':
        tours_queryset = tours_queryset.annotate(
            calculated_duration=ExpressionWrapper(
                F('date_end') - F('date_start'),
                output_field=DurationField()
            )
        ).order_by('-calculated_duration')

    # Настраиваем пагинацию: по 10 туров на страницу
    paginator = Paginator(tours_queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'current_sort': sort_by,
        'filters': filters,
    }

    return render(request, 'catalog.html', context)


def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    reviews = Review.objects.filter(tour=tour).order_by('-created_at')
    form = ReviewForm()

    if hasattr(tour, 'services') and tour.services:
        services = [s.strip() for s in tour.services.split(',') if s.strip()]
    else:
        services = []
    add_services = AddService.objects.all()

    user_has_booked = False
    if request.user.is_authenticated:
        user_has_booked = Booking.objects.filter(user=request.user, tour=tour).exists()

    # Находим похожие туры. Обычным пользователям не подмешиваем архивные туры в рекомендации
    current_date = timezone.now().date()
    if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
        base_similar = Tour.objects.all()
    else:
        base_similar = Tour.objects.filter(date_end__gte=current_date)

    similar_tours = base_similar.filter(country=tour.country).exclude(pk=tour.pk)[:3]

    if similar_tours.count() < 3:
        additional_tours = base_similar.exclude(pk=tour.pk).exclude(country=tour.country)[:3 - similar_tours.count()]
        similar_tours = list(similar_tours) + list(additional_tours)

    return render(request, 'tour_detail.html', {
        'tour': tour,
        'reviews': reviews,
        'form': form,
        'similar_tours': similar_tours,
        'user_has_booked': user_has_booked,
        'services': services,
        'add_services': add_services,
    })


@login_required
def add_review(request, pk):
    tour = get_object_or_404(Tour, pk=pk)

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
    tour = get_object_or_404(Tour, pk=tour_id)
    header_settings = HeaderSettings.objects.first()

    if request.method == 'POST':
        form = BookingForm(request.POST)

        if tour.slots_left <= 0 or tour.is_expired:
            messages.error(request, "К сожалению, этот тур уже недоступен для бронирования.")
            return redirect('tour_detail', pk=tour_id)

        if form.is_valid():
            people_count = form.cleaned_data['people_count']
            user_comment = form.cleaned_data['user_comment']

            current_booked = tour.booked_slots if tour.booked_slots is not None else 0
            current_total = tour.total_slots if tour.total_slots is not None else 20
            available_slots = current_total - current_booked

            if available_slots >= people_count:
                Booking.objects.create(
                    user=request.user,
                    tour=tour,
                    people_count=people_count,
                    user_comment=user_comment
                )

                tour.booked_slots = current_booked + people_count
                tour.save()

                # ОТПРАВКА ПИСЬМА О БРОНИРОВАНИИ ТУРА
                if request.user.email:
                    subject = "Спасибо за заказ! | Tralley-Valley"
                    message = (
                        f"Здравствуйте, {request.user.username}!\n\n"
                        f"Спасибо за ваш заказ на сайте Tralley-Valley!\n"
                        f"Вы успешно забронировали тур '{tour.name}' ({tour.country}) на {people_count} чел.\n\n"
                        f"⏳ Мы уже начали оформление документов. Скоро мы пришлем ваши билеты и ваучеры! "
                        f"Они будут доступны для скачивания в вашем личном кабинете за 2-3 дня до вылета.\n\n"
                        f"Приятного ожидания путешествия! ✈️\n\n"
                        f"С уважением, команда Tralley-Valley"
                    )
                    try:
                        send_mail(
                            subject=subject,
                            message=message,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[request.user.email],
                            fail_silently=True,
                        )
                    except Exception:
                        pass

                messages.success(request, f"Тур '{tour.name}' успешно забронирован!")
                return redirect('profile')
            else:
                form.add_error('people_count', f"Недостаточно мест. Доступно всего: {available_slots}")
    else:
        form = BookingForm()

    return render(request, 'booking.html', {
        'tour': tour,
        'header_settings': header_settings,
        'form': form
    })


@login_required
def profile_view(request):
    user_bookings = Booking.objects.filter(user=request.user).select_related('tour')
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'profile.html', {
        'user': request.user,
        'bookings': user_bookings,
        'reviews': reviews,
    })


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'profile_edit.html', {'form': form})