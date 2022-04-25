from ..commands import *
import requests


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("creating admin user...")
        user = User.objects.filter(username="admin2").count()
        if user:
            return

        User.objects.create_superuser(
            email="admin2@sary.com",
            username="admin2",
            password="P@ssw0rd",
            employee_number=1234
        )
