from .models import HeaderSettings

def load_header(request):
    return {
        'header_settings': HeaderSettings.objects.first()
    }