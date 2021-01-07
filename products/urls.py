from django.urls import path
from .views import ProductListView, ProductDetailView,\
    ProductCreateView, ProductUpdateView, ProductDeleteView,\
    MyProductView
urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='detail'),
    path('<slug:slug>/update', ProductUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete', ProductDeleteView.as_view(), name='delete'),
    path('dashboard/myproducts/', MyProductView.as_view(), name='my_products'),
]
