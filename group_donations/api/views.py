from django.contrib.auth import get_user_model
from django.core.cache import cache
from djoser.views import UserViewSet
from rest_framework import permissions, viewsets

from collect_payments.models import Collect, Payment, Reason
from .pagination import LimitOnPagePagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (CollectSerializer, PaymentSerializer,
                          ReasonCreateSerializer, ReasonSerializer)
from .tasks import (send_collection_successfully_created_email_task,
                    send_payment_successfully_created_email_task)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    pagination_class = None

    def get_permissions(self):
        if self.action == 'me':
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()


class ReasonViewSet(viewsets.ModelViewSet):
    queryset = Reason.objects.all()
    serializer_class = ReasonSerializer
    pagination_class = None
    permission_classes = (IsAuthorOrReadOnly, )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return super().get_serializer_class()
        return ReasonCreateSerializer


class CollectViewSet(viewsets.ModelViewSet):
    cache_key = 'collect'
    cache_time = 60 * 10
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    pagination_class = LimitOnPagePagination
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        cache.delete(self.cache_key)
        send_collection_successfully_created_email_task(self.request)
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        cache_list = cache.get(self.cache_key)
        response = super().list(request, *args, **kwargs)
        if cache_list:
            response.data = cache_list
        else:
            cache.set(self.cache_key, response.data, self.cache_time)
        return response


class PaymentViewSet(viewsets.ModelViewSet):
    cache_key = 'payment'
    cache_time = 60 * 10
    serializer_class = PaymentSerializer
    pagination_class = LimitOnPagePagination
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        collect_id = self.request.query_params.get('collect_id')
        queryset = Payment.objects.filter(collect=collect_id)
        return queryset

    def perform_create(self, serializer):
        cache.delete(self.cache_key)
        send_payment_successfully_created_email_task(self.request)
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        cache_list = cache.get(self.cache_key)
        response = super().list(request, *args, **kwargs)
        if cache_list:
            response.data = cache_list
        else:
            cache.set(self.cache_key, response.data, self.cache_time)
        return response
