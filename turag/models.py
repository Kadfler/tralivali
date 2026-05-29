from datetime import date
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    tour_id = models.ForeignKey('Tour', on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    add_service_id = models.ForeignKey('AddService', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} — {self.tour_id}"


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tour_id = models.ForeignKey('Tour', on_delete=models.CASCADE)
    title = models.TextField()
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class AddService(models.Model):
    add_service_id = models.AutoField(primary_key=True)
    name = models.TextField()
    content = models.TextField()
    # Защитили стоимость от отрицательных значений
    cost = models.IntegerField(
        validators=[MinValueValidator(0, message="Стоимость услуги не может быть отрицательной!")]
    )

    def __str__(self):
        return self.name


class Transport(models.Model):
    transport_id = models.AutoField(primary_key=True)
    name = models.TextField()
    carrier = models.TextField()
    type = models.TextField()
    way = models.TextField()

    def __str__(self):
        return self.name


class Hotel(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    name = models.TextField()
    address = models.TextField()
    country = models.TextField(default="")
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class TourOperator(models.Model):
    tour_operator_id = models.AutoField(primary_key=True)
    name = models.TextField()
    address = models.TextField()
    site = models.TextField()
    email = models.TextField()
    country = models.TextField(default="")

    def __str__(self):
        return self.name


class Tour(models.Model):
    tour_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=200, verbose_name="Название тура")
    description = models.TextField()
    hotel_id = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    transport_id = models.ForeignKey('Transport', on_delete=models.CASCADE)
    program_id = models.ForeignKey('Program', on_delete=models.CASCADE)
    tour_operator_id = models.ForeignKey('TourOperator', on_delete=models.CASCADE)
    date_start = models.DateTimeField(verbose_name="Дата начала")
    date_end = models.DateTimeField(verbose_name="Дата окончания")

    # ИСПРАВЛЕНО: Убран ошибочный параметр max_length
    cost_for_one_person = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость за одного человека",
        validators=[MinValueValidator(0, message="Цена тура не может быть отрицательной!")]
    )
    persons = models.PositiveIntegerField(default=0)
    image_url = models.URLField(max_length=500, verbose_name="Ссылка на фото товара", default="")
    total_slots = models.PositiveIntegerField(default=20, verbose_name="Всего мест")
    booked_slots = models.PositiveIntegerField(default=0, verbose_name="Занято мест")

    @property
    def duration(self):
        if self.date_start and self.date_end:
            # ИСПРАВЛЕНО: Извлекаем чистые даты перед вычитанием, чтобы получить дни без микросекунд
            delta = self.date_end.date() - self.date_start.date()
            days = delta.days

            if days % 10 == 1 and days % 100 != 11:
                return f"{days} день"
            elif 2 <= days % 10 <= 4 and not (12 <= days % 100 <= 14):
                return f"{days} дня"
            else:
                return f"{days} дней"
        return "Не указана"

    @property
    def is_expired(self):
        if self.date_start:
            try:
                return self.date_start.date() < date.today()
            except AttributeError:
                return self.date_start < date.today()
        return False

    @property
    def slots_left(self):
        return max(0, self.total_slots - self.booked_slots)

    # ИСПРАВЛЕНО: Превратили в @property для корректной работы шаблонов
    @property
    def avg_rating(self):
        reviews = self.reviews.all()
        if not reviews.exists():
            return 0
        return round(sum(r.rating for r in reviews) / reviews.count(), 1)

    # ИСПРАВЛЕНО: Превратили в @property для корректной работы шаблонов
    @property
    def reviews_count(self):
        return self.reviews.count()

    # ИСПРАВЛЕНО: Убрана ошибочная попытка перезаписи свойства duration
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='review_photos/', blank=True, null=True, verbose_name="Фото к отзыву")

    def __str__(self):
        return f'{self.user.username} - {self.tour.name}'


class Program(models.Model):
    program_id = models.AutoField(primary_key=True)
    name = models.TextField()
    services = models.TextField()
    description = models.TextField()
    hotel_id = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    city = models.TextField()
    meal = models.TextField()
    activities = models.TextField()

    def __str__(self):
        return self.name


class HeaderSettings(models.Model):
    title = models.CharField(max_length=100, default="Настройки шапки", editable=False)
    background_image = models.ImageField(upload_to='headers/', verbose_name="Фоновое изображение шапки")

    class Meta:
        verbose_name = "Настройки шапки"
        verbose_name_plural = "Настройки шапки"

    def __str__(self):
        return self.title


class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name="Тур")
    people_count = models.IntegerField(default=1, verbose_name="Количество человек")
    user_comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата бронирования")

    def __str__(self):
        return f"{self.user} - {self.tour.name}"