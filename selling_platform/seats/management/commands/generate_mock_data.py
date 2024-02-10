from datetime import timedelta
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth import get_user_model
from seats.models import Price, Ticket, Stadium, Seat, Match

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

    def create_stadiums(self, num_stadiums):
        for _ in range(num_stadiums):
            Stadium.objects.create(description=fake.word())

    def create_matches(self, num_matches):
        import time
        time.sleep(2)
        stadiums = Stadium.objects.all()

        for _ in range(num_matches):
            start_time = fake.date_time_this_year()
            end_time = start_time + timedelta(hours=fake.random_int(min=1, max=4))
            stadium = fake.random_element(elements=stadiums)

            # Ensure no overlapping intervals for matches in the same stadium
            while Match.objects.filter(stadium=stadium, start_time__lt=end_time, end_time__gt=start_time).exists():
                start_time = fake.date_time_this_year()
                end_time = start_time + timedelta(hours=fake.random_int(min=1, max=4))

            # Create the Match instance with the associated Stadium
            match = Match.objects.create(start_time=start_time, end_time=end_time, stadium=stadium)

    # def create_matches(self, num_matches):
    #     import time
    #     time.sleep(2)
    #     stadiums = Stadium.objects.all()
    #
    #     for _ in range(num_matches):
    #         start_time = fake.date_time_this_year()
    #         end_time = start_time + timedelta(hours=fake.random_int(min=1, max=4))
    #         stadium = fake.random_element(elements=stadiums)
    #
    #         # Ensure no overlapping intervals for matches in the same stadium
    #         while Match.objects.filter(stadium=stadium, start_time__lt=end_time, end_time__gt=start_time).exists():
    #             start_time = fake.date_time_this_year()
    #             end_time = start_time + timedelta(hours=fake.random_int(min=1, max=4))
    #
    #         # Create the Match instance
    #         match = Match.objects.create(start_time=start_time, end_time=end_time)
    #
    # Associate the stadium with the match using .set()
    # match.stadium.set([stadium])

    def create_seats(self, num_seats):
        stadiums = Stadium.objects.all()
        for _ in range(num_seats):
            Seat.objects.create(seat_number=fake.random_int(min=1, max=100),
                                stadium=fake.random_element(elements=stadiums))

    def handle(self, *args, **kwargs):
        # Create superuser
        self.stdout.write(self.style.SUCCESS('Creating superuser...'))
        self.create_superuser()

        # Number of instances you want to create for each model
        num_prices = 10
        num_seats = 50
        num_stadiums = 5
        num_matches = 20

        # Create Price instances
        self.stdout.write(self.style.SUCCESS('Creating Price instances...'))
        for _ in range(num_prices):
            predefined_words = ['VPI', 'economy', 'Mid']
            _name = fake.random_element(elements=predefined_words),

            Price.objects.create(
                name=_name,
                unit_price=fake.pydecimal(left_digits=3, right_digits=2, positive=True),
            )

        # Create Stadium instances
        self.stdout.write(self.style.SUCCESS('Creating Stadium instances...'))
        self.create_stadiums(num_stadiums)

        # Create Match instances
        self.stdout.write(self.style.SUCCESS('Creating Match instances...'))
        self.create_matches(num_matches)

        # Create Seat instances
        self.stdout.write(self.style.SUCCESS('Creating Seat instances...'))
        self.create_seats(num_seats)

        # Create Ticket instances
        self.stdout.write(self.style.SUCCESS('Creating Ticket instances...'))
        users = get_user_model().objects.all()
        for _ in range(num_seats):
            Ticket.objects.create(
                created_at=fake.date_time_this_year(),
                price=fake.random_element(elements=Price.objects.all()),
                status=4,
                user=fake.random_element(elements=[None] + list(users)),
                match=fake.random_element(elements=Match.objects.all()),
                seat=fake.random_element(elements=Seat.objects.all()),
                stadium=fake.random_element(elements=Stadium.objects.all()),
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated mock data'))
