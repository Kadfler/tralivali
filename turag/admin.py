from django.contrib import admin
from .models import Tour, Program, Hotel, Transport, AddService, TourOperator, HeaderSettings


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    # В таблице списков (отображаются свойства и поля)
    list_display = ('name', 'country', 'duration', 'cost_for_one_person')
    search_fields = ('name', 'country')
    list_filter = ('country',)

    # Полный список ВСЕХ полей, которые теперь появятся при создании и редактировании тура
    fields = (
        'name',
        'country',
        'description',
        'hotel_id',
        'transport_id',
        'program_id',
        'tour_operator_id',
        'date_start',
        'date_end',
        'cost_for_one_person',
        'persons',
        'image_url',
        'total_slots',
    )

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

@admin.register(HeaderSettings)
class HeaderSettingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'background_image')
    search_fields = ('title', 'background_image')