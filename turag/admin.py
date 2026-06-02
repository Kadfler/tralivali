from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Импортируйте все модели.
# Убедитесь, что Booking и Review импортированы из вашего models.py
from .models import (
    Tour, Program, Hotel, Transport, AddService,
    TourOperator, HeaderSettings, Booking, Review, TourImage
)
from image_uploader_widget.widgets import ImageUploaderWidget

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')

class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1

# --- 2. Бронирования ---
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tour', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'tour__name')
    list_editable = ('status',)  # Быстрая смена статуса в списке


# --- 3. Отзывы ---
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'text')

    # Добавьте этот метод, чтобы виджет заработал для отзывов
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'image':  # Или как называется ваше поле с фото в Review
            kwargs['widget'] = ImageUploaderWidget
        return super().formfield_for_dbfield(db_field, **kwargs)


# --- 4. Остальные модели ---
@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'duration', 'cost_for_one_person')
    search_fields = ('name', 'country')
    list_filter = ('country',)
    readonly_fields = ('slug',)
    inlines = [TourImageInline]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'image':
            kwargs['widget'] = ImageUploaderWidget
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(AddService)
class AddServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost')


@admin.register(TourOperator)
class TourOperatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')


@admin.register(HeaderSettings)
class HeaderSettingsAdmin(admin.ModelAdmin):
    list_display = ('title',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'background_image':
            kwargs['widget'] = ImageUploaderWidget
        return super().formfield_for_dbfield(db_field, **kwargs)