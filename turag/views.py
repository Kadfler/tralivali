from django.shortcuts import render, get_object_or_404
from .models import Tour

def index(request):
    return render(request, 'index.html')

def catalog(request):
    tours = Tour.objects.all()

    name = request.GET.get('name', '').strip()
    country = request.GET.get('country', '').strip()
    duration = request.GET.get('duration', '').strip()
    persons = request.GET.get('persons', '').strip()

    if name:
        tours = tours.filter(name__icontains=name)

    if country:
        tours = tours.filter(country__icontains=country)

    if duration:
        tours = tours.filter(program_id__duration=duration)

    if persons:
        tours = tours.filter(cost_for_one_person=persons)

    return render(request, 'catalog.html', {
        'tours': tours,
        'name': name,
        'country': country,
        'duration': duration,
        'people': persons,
    })

def tour_card(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    return render(request, 'card.html', {'tour': tour})