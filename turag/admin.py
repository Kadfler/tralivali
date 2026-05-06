from django.contrib import admin
from .models import Tour, Program, Hotel, Transport, AddService, TourOperator

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'duration', 'persons', 'cost_for_one_person')
    search_fields = ('name', 'country')
    list_filter = ('country', 'duration', 'persons')
    exclude = ('comments',)

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country')
    list_filter = ('country',)

@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(AddService)
class AddServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost')
    search_fields = ('name',)
    list_filter = ('cost',)

@admin.register(TourOperator)
class TourOperatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country')
    list_filter = ('country',)