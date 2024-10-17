from django.urls import path

from apps.order.views import CreateOrderView


urlpatterns = [
    path('create-list/', CreateOrderView.as_view())
]