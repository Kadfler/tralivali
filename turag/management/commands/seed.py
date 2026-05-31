import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from faker import Faker
from turag.models import Tour  # Импортируем твою модель туров
# Импортируем модели отелей, транспорта, программ и туроператоров для связей
from turag.models import Hotel, Transport, Program, TourOperator


class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми турами для Tralley-Valley'

    def handle(self, *args, **kwargs):
        fake = Faker('ru_RU')

        # Проверяем, есть ли связанные записи, чтобы ForeignKey не вызвали ошибку.
        # Если их нет — берем первый попавшийся или создаем базовую заглушку.
        hotel = Hotel.objects.first() or Hotel.objects.create(name="Тестовый отель", address="Улица Тестовая")
        transport = Transport.objects.first() or Transport.objects.create(name="Самолет Экспресс", carrier="АвиаЛинии",
                                                                          type="Авиа", way="Прямой")
        program = Program.objects.first() or Program.objects.create(name="Обзорная программа", services="Экскурсии",
                                                                    description="Описание", hotel_id=hotel,
                                                                    city="Москва", meal="Завтраки",
                                                                    activities="Прогулки")
        operator = TourOperator.objects.first() or TourOperator.objects.create(name="Главный Оператор", address="Офис",
                                                                               site="site.ru", email="op@site.ru")

        tour_names = [
            'Золотое кольцо Алтая',
            'Выходные на Байкале',
            'Огни ночного Дубая',
            'Тайны древнего Египта',
            'Прогулки по Стамбулу',
            'Релакс на Мальдивах',
            'Экзотический Пхукет',
            'Высокогорный Дагестан',
            'Карельские сказки',
            'Солнечный Сочи Экспресс',
        ]

        countries = ['Россия', 'ОАЭ', 'Египет', 'Турция', 'Мальдивы', 'Таиланд']

        self.stdout.write('Начинаю заполнение базы данных турами...')

        for _ in range(15):
            # Генерируем даты начала и конца
            date_start = fake.date_between(start_date='+5d', end_date='+30d')
            duration_days = random.randint(3, 14)
            date_end = date_start + timedelta(days=duration_days)

            # Выбираем случайное количество мест
            total_slots = random.randint(15, 30)
            # Случайно забиваем места, иногда делая тур полностью забронированным
            booked_slots = random.choice([total_slots, random.randint(0, total_slots - 1)])

            Tour.objects.create(
                name=random.choice(tour_names),
                country=random.choice(countries),
                description=fake.text(max_nb_chars=250),

                # УДАЛЕНО ПОЛЕ duration: Django сам его посчитает на основе переданных ниже дат!
                date_start=date_start,
                date_end=date_end,

                cost_for_one_person=random.randint(25000, 150000),

                # ИСПРАВЛЕНО: Передаем реальные поля количества мест
                total_slots=total_slots,
                booked_slots=booked_slots,

                # Передаем обязательные внешние ключи (ForeignKey)
                hotel_id=hotel,
                transport_id=transport,
                program_id=program,
                tour_operator_id=operator,
                persons=random.randint(1, 3)
            )

        self.stdout.write(
            self.style.SUCCESS(
                'База данных Tralley-Valley успешно заполнена тестовыми турами!'
            )
        )