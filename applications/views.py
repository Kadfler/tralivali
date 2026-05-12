from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ApplicationForm
from .models import Application

@login_required
def create_application_view(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            return redirect('applications')
    else:
        form = ApplicationForm()

    return render(request, 'applications/create.html', {'form': form})

@login_required
def applications_view(request):
    applications = Application.objects.filter(user=request.user)
    return render(request, 'applications/list.html', {'applications': applications})