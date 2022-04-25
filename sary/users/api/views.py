from datetime import (
    datetime,
    timezone,
    timedelta
)

from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (
    IsAdminUser
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import (
    UserSerializer,
    TableSerializer,
    ReservationSerializer
)
from ..models import (
    Table,
    Reservation
)


User = get_user_model()


class UserViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    # def get_queryset(self, *args, **kwargs):
    #     assert isinstance(self.request.user.id, int)
    #     return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=['post'])
    def me(self, request):
        serializer = UserSerializer(data=request.data, context={'request': request})
        serializer.is_valid()
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class TableViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = TableSerializer
    queryset = Table.objects.all()


class ReservationViewSet(ModelViewSet):

    def get_queryset(self) -> QuerySet:
        # By default would all reservation
        #
        queryset = Reservation.objects.all()
        is_all = self.request.query_params.get('all', True)
        sort_order = self.request.query_params.get('order')
        table_id = self.request.query_params.get('table_id')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if is_all == 'False':
            queryset = queryset.filter(start_date__gte=datetime.now().replace(tzinfo=None))
        if sort_order == 'asc':
            queryset = queryset.order_by('start_date')
        else:
            queryset = queryset.order_by('-start_date')

        if table_id:
            if not self.request.user.is_staff:
                raise ValidationError(detail="Reservation by table ID to non Admin user not allowed")
            queryset = queryset.filter(table_id=table_id)

        if start_date and end_date:
            if not self.request.user.is_staff:
                raise ValidationError(detail="Date filter not allowed to non admin user")
            queryset = queryset.filter(table_id=table_id)
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
                end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                raise ValidationError(detail="Date format incorrect")

            queryset = queryset.filter(Q(start_date__gte=start_date.replace(tzinfo=timezone.utc))
                                       & Q(end_date__lte=end_date.replace(tzinfo=timezone.utc)))

        return queryset

    permission_classes = (IsAdminUser,)
    serializer_class = ReservationSerializer
    # queryset = Reservation.objects.all()

    @action(detail=False, methods=['post'])
    def reserve_time(self, request):

        res_ser = ReservationSerializer(data=request.data)
        res_ser.is_valid(raise_exception=True)

        start_date = datetime.strptime(request.data.get('start_date'), '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(request.data.get('end_date'), '%Y-%m-%d %H:%M:%S')

        table_id = request.data.get('id')

        if start_date > end_date:
            raise ValidationError(detail='End Date should always be ahead of Start date')

        table = Table.objects.filter(id=table_id)
        if not table:
            raise ValidationError(detail='Invalid ID of table')

        table_res = Reservation.objects.filter(Q(table_id=table[0].id) &
                                               (Q(start_date__lt=start_date.replace(tzinfo=timezone.utc)) &
                                                Q(end_date__gt=start_date.replace(tzinfo=timezone.utc))) |
                                               (Q(start_date__lt=end_date.replace(tzinfo=timezone.utc)) &
                                                Q(end_date__gt=end_date.replace(tzinfo=timezone.utc))))

        if table_res:
            raise ValidationError(detail='Reservation Already Exist')
        reservation = Reservation.objects.create(table=table[0], start_date=start_date.replace(tzinfo=timezone.utc),
                                                 end_date=end_date.replace(tzinfo=timezone.utc))
        return Response({'status': status.HTTP_200_OK})

    @action(detail=False, methods=['get'])
    def get_time_slot(self, request):

        requested_seat = self.request.query_params.get('requested_seat')

        table = Table.objects.filter(no_of_chair__lte=requested_seat).order_by('-no_of_chair').first()
        reservation = None
        if table:
            reservation = Reservation.objects.filter(table=table,
                                                     start_date__gt=datetime.now().replace(hour=12, minute=0)).order_by('start_date')

        else:
            raise ValidationError(detail='No table with requested seat are available')

        (datetime.now() - datetime.now().replace(tzinfo=None) + timedelta(hours=1))

        free_slots = []
        resr_len = len(reservation)
        for index, resr in enumerate(reservation):
            free_slots.append({
                "no_of_chair": table.no_of_chair,
                "start_slot":  datetime.now().replace(tzinfo=None) if index == 0 else reservation[index - 1].end_date,
                "end_slot": datetime.now().replace(tzinfo=None, hour=23, minute=59)
                if index == (resr_len - 1) else resr.start_date if index == 0 else resr.start_date
            })

        return Response(free_slots)
