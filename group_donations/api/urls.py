from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CollectViewSet, CustomUserViewSet, PaymentViewSet,
                    ReasonViewSet)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('collects', CollectViewSet, basename='collects')
router_v1.register('payments', PaymentViewSet, basename='payments')
router_v1.register('reasons', ReasonViewSet, basename='reasons')
router_v1.register('users', CustomUserViewSet, basename='users')


urlpatterns = [
    path('', include(router_v1.urls)),
]
