from django.urls import path

from apps.product.views import ProductCreateView, ProductListView, ProductDetailView, ProductUpdateView

urlpatterns = [
    path('create/', ProductCreateView.as_view()),
    path('list/', ProductListView.as_view()),
    path('detail/<int:pk>/', ProductDetailView.as_view()),
    path('update/<int:pk>/', ProductUpdateView.as_view())
]