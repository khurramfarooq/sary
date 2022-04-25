from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from sary.users.api.views import (
    UserViewSet,
    TableViewSet,
    ReservationViewSet
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("table", TableViewSet)
router.register("reservation", ReservationViewSet, basename="table-reservation")


app_name = "api"
urlpatterns = router.urls
