from django.db import models
from django.conf import settings

class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('process', 'В обработке'),
        ('done', 'Завершена'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('card', 'Карта'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=200)
    start_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f'{self.course_name} — {self.user.username}'