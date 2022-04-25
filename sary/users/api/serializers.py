from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from ..models import (
    Table,
    Reservation
)
from datetime import (
    date,
    datetime
)
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "employee_number", "name", "url", "password"]
        username = serializers.ModelSerializer(required=True)
        password = serializers.CharField(
            max_length=68, min_length=6, write_only=True)
        employee_number = serializers.IntegerField(max_value=9999, min_value=1000, required=False)
        username = serializers.CharField(required=False)

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        print("creating user...")
        return make_password(value)

    def validate_employee_number(self, value: int) -> int:
        if value >= 9999 or value <= 1000:
            raise ValidationError(detail="Employee Number should be of 4 digit")
        return value


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ["id", "no_of_table", "no_of_chair"]

    def validate_no_of_chair(self, value: int) -> int:
        if 1 <= value <= 12:
            return value
        raise ValidationError(detail="Number of chair should be between 1 and 12")


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "start_date", "end_date"]

        id = serializers.IntegerField(required=True)

    def validate_start_date(self, value: str) -> str:
        start_date = value.replace(tzinfo=None)
        res_open_time = datetime.now()
        res_open_time = res_open_time.replace(hour=12, minute=00)

        if start_date < res_open_time:
            raise ValidationError(detail="Date exceeds restaurant timing")
        return value

    def validate_end_date(self, value: str) -> str:
        end_date = value.replace(tzinfo=None)
        res_close_time = datetime.now()
        res_close_time = res_close_time.replace(hour=23, minute=59)

        if end_date > res_close_time:
            raise ValidationError(detail="Date exceeds restaurant timing")
        return value
