from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from collect_payments.models import Collect, Payment, Reason

User = get_user_model()
faker = Faker(['en-US', 'ru-RU'])


class Command(BaseCommand):
    help = 'Заполняет базу данных моковыми значениями'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Число моковых данных')

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(
            'Старт команды. База данных заполняется'
        ))
        count = int(options['count'])

        reasons = [Reason(
            name=faker.words(nb=2, unique=True),
            color=faker.hex_color(),
            slug=faker.slug()
        ) for _ in range(count)]
        Reason.objects.bulk_create(reasons)

        users = [User(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            surname=faker.middle_name(),
            username=faker.user_name(),
            password=faker.password(),
            email=faker.email()
        ) for _ in range(count)]
        User.objects.bulk_create(users)

        collects = [Collect(
            author=User.objects.first(),
            name=faker.sentence(),
            reason=Reason.objects.last(),
            description=faker.text(),
            planned_amount=faker.pydecimal(
                left_digits=3, right_digits=2, positive=True
            ),
            cover_image=faker.file_path(depth=2, category='image'),
            pub_date=faker.date_time(),
            end_date=faker.future_datetime()
        ) for _ in range(count)]
        Collect.objects.bulk_create(collects)

        payments = [Payment(
            user=User.objects.last(),
            amount=faker.pydecimal(
                left_digits=3, right_digits=2, positive=True
            ),
            comments=faker.text(),
            created_at=faker.date_time(),
            collect=Collect.objects.first()
        ) for _ in range(count)]
        Payment.objects.bulk_create(payments)

        self.stdout.write(self.style.SUCCESS('Данные загружены.'))
