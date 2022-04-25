from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from psycopg2.extras import DateTimeTZRange


class User(AbstractUser):
    """
    Default custom user model for assesment.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    is_active = models.BooleanField(default=True)
    employee_number = models.IntegerField(max_length=4, default=0000)

    USERNAME_FIELD = 'employee_number'

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Table(models.Model):
    no_of_table = models.IntegerField()
    no_of_chair = models.IntegerField()


class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="table_reservation")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
