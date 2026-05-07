from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


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
    cost = models.IntegerField()

    def __str__(self):
        return self.name

class Transport(models.Model):
    transport_id = models.AutoField(primary_key=True)
    name = models.TextField()
    carrier= models.TextField()
    type = models.TextField()
    way= models.TextField()

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
    name = models.TextField()
    description = models.TextField()
    hotel_id = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    transport_id = models.ForeignKey('Transport', on_delete=models.CASCADE)
    program_id = models.ForeignKey('Program', on_delete=models.CASCADE)
    tour_operator_id = models.ForeignKey('TourOperator', on_delete=models.CASCADE)
    date_start = models.DateTimeField(auto_now_add=True)
    date_end = models.DateTimeField(auto_now_add=True)
    cost_for_one_person = models.IntegerField(default=0)
    duration = models.PositiveIntegerField(default=0)
    persons = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='tours/', blank=True, null=True)

    def avg_rating(self):
        reviews = self.reviews.all()
        if not reviews.exists():
            return 0
        return round(sum(r.rating for r in reviews) / reviews.count(), 1)

    def reviews_count(self):
        return self.reviews.count()

    def save(self, *args, **kwargs):
        if self.date_start and self.date_end:
            self.duration = (self.date_end - self.date_start).days
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

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

