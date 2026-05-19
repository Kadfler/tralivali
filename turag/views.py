from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Tour, Review, HeaderSettings, Booking
from .forms import ReviewForm

def index(request):
    return render(request, 'index.html')

def tour_card(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    return render(request, 'card.html', {'tour': tour})


def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)

    # Вытаскиваем отзывы из БД, чтобы они вывелись через {% for review in reviews %}
    reviews = Review.objects.filter(tour=tour).order_by('-created_at')

    # Создаем пустую форму, чтобы на странице появились {{ form.rating }} и {{ form.text }}
    form = ReviewForm()

    context = {
        'tour': tour,
        'reviews': reviews,
        'form': form,  # <-- Без этого поля формы будут невидимыми!
    }
    return render(request, 'tour_detail.html', context)


def catalog_view(request):
    # Берем первую загруженную настройку (или None, если админ еще ничего не загрузил)
    header_settings = HeaderSettings.objects.first()
    tours = Tour.objects.all()  # ваш текущий код

    return render(request, 'catalog.html', {
        'tours': tours,
        'header_settings': header_settings
    })

def catalog(request):
    tours = Tour.objects.all().order_by('-tour_id')

    destination = request.GET.get('destination', '').strip()
    check_in = request.GET.get('check_in', '').strip()
    check_out = request.GET.get('check_out', '').strip()
    cost_for_one_person = request.GET.get('cost_for_one_person', '').strip()

    if destination:
        tours = tours.filter(name__icontains=destination)

    if check_in:
        tours = tours.filter(date_start__gte=check_in)

    if check_out:
        tours = tours.filter(date_end__lte=check_out)

    if cost_for_one_person:
        tours = tours.filter(cost_for_one_person=cost_for_one_person)

    return render(request, 'catalog.html', {
        'tours': tours,
        'filters': {
            'destination': destination,
            'check_in': check_in,
            'check_out': check_out,
            'cost_for_one_person': cost_for_one_person or 500,
        }
    })


@login_required
def add_review(request, pk):
    tour = get_object_or_404(Tour, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.tour = tour
            review.user = request.user
            review.save()

    return redirect('tour_detail', pk=pk)


@login_required
def book_tour_view(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)

    if request.method == 'POST':

        people_count = request.POST.get('people_count', 1)
        user_comment = request.POST.get('user_comment', '')

        Booking.objects.create(
            user=request.user,
            tour=tour,
            people_count=people_count,
            user_comment=user_comment
        )
        return redirect('profile')

    return render(request, 'booking.html', {'tour': tour})

@login_required
def profile_view(request):

    user_bookings = Booking.objects.filter(user=request.user).select_related('tour')

    context = {
        'user': request.user,
        'bookings': user_bookings,
    }
    return render(request, 'profile.html', context)