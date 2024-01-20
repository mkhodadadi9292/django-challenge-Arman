# yourapp/management/commands/generate_mock_data.py
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth import get_user_model
from seats.models import Price, Seat

fake = Faker()


class Command(BaseCommand):
    help = 'Generate mock data for the seats app'

    def create_superuser(self):
        username = "admin"
        password = "admin"
        email = "admin@example.com"  # You can change this email as needed

        try:
            user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            get_user_model()._default_manager.db_manager().create_superuser(
                username=username, email=email, password=password
            )
            self.stdout.write(self.style.SUCCESS('Superuser created: username=admin, password=admin'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists: username=admin, password=admin'))

    def handle(self, *args, **kwargs):
        # Create superuser
        self.stdout.write(self.style.SUCCESS('Creating superuser...'))
        self.create_superuser()

        # Number of instances you want to create for each model
        num_prices = 10
        num_seats = 50

        # Create Price instances
        for _ in range(num_prices):
            Price.objects.create(
                name=fake.word(),
                unit_price=fake.pydecimal(left_digits=3, right_digits=2, positive=True),
            )

        # Create Seat instances
        users = get_user_model().objects.all()
        for _ in range(num_seats):
            Seat.objects.create(
                created_at=fake.date_time_this_year(),
                type=fake.random_int(min=1, max=5),
                price=fake.random_element(elements=Price.objects.all()),
                status=fake.random_element(elements=[1, 2, 3, 4]),
                user=fake.random_element(elements=[None] + list(users)),
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated mock data'))
