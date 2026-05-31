from django.contrib import admin
from django.db import models
from .models import Tour, Program, Hotel, Transport, AddService, TourOperator, HeaderSettings
from image_uploader_widget.widgets import ImageUploaderWidget  # <-- ИМПОРТ КРАСИВОГО ВИДЖЕТА

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'duration', 'cost_for_one_person')
    search_fields = ('name', 'country')
    list_filter = ('country',)

    readonly_fields = ('slug',)

    fields = (
        'name',
        'slug',  # Добавили отображение слага в админке
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
        'image',  # Поменяли image_url на image
        'total_slots',
    )

    # Принудительно подключаем красивый виджет для картинок
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'image':
            kwargs['widget'] = ImageUploaderWidget
        return super().formfield_for_dbfield(db_field, **kwargs)


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

    # И для шапки сайта тоже делаем красивую загрузку картинки
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'background_image':
            kwargs['widget'] = ImageUploaderWidget
        return super().formfield_for_dbfield(db_field, **kwargs)