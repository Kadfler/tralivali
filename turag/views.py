from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Tour, Review
from .forms import ReviewForm

def index(request):
    return render(request, 'index.html')

def tour_card(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    return render(request, 'card.html', {'tour': tour})

def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    return render(request, 'tour_detail.html', {'tour': tour})


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