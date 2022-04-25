# assesment

Assesment Sary

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your app locally

- Browse to root folder of the project and simply run the below command for the local setup.

        $ docker-compose -f local.yml build
        $ docker-compose -f local.yml up

The above command will create the superuser with the credentials as below:

`employeeNumber: 1234, password:P@ssw0rd`

### API token JWT

####Below API would get you the token to validate the user:
- JSON Format
``http://localhost:8000/api/token/``

```{"employee_number": "1234", "password": "P@ssw0rd"}```

### Create, Get, Delete Table

####Below API would get you the token to validate the user:
- JSON Format POST
``http://localhost:8000/api/table/``

```{"no_of_table": "2", "no_of_chair": "4"}```

### Create, Get, Delete Reservation

#### Below API would get you the token to validate the user:
- JSON Format POST
``http://localhost:8000/api/reservation/reserve_time/``

```{"id": 1, "start_date": "2022-04-25 13:30:00", "end_date": "2022-04-25 14:00:00"}```

#### API to get Reservation
-  GET
``http://localhost:8000/api/reservation/``


#### API to get available slot time for the table when user enter requested seat by the customer
- GET
``http://localhost:8000/api/reservation/get_time_slot/?requested_seat=6``



### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

