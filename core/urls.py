from django.urls import path
from core import views
from .views import (
    ItemDetailView,
    CheckoutView,
    HomeView,
    CategoryView,
    OrderSummaryView,
    CustOrders,
    AddView,
    DelView,
    Delete,
    UpdView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
)

app_name = 'core'

urlpatterns = [
    path('', views.home, name='core_home'),
    path('homeview/', HomeView.as_view(), name='home'),
    path('categoryview/<int:category_id>', CategoryView.as_view(), name='category'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-product/', AddView.as_view(), name='add-product'),
    path('delete', Delete.as_view(), name='delete'),
    path('delete-product/<int:pk>', DelView.as_view(), name='delete-product'),
    path('update-order/<int:pk>', UpdView.as_view(), name='update-order'),
    path('cust-orders/', views.CustOrders, name='cust-orders'),
    path('orders/', views.OrdersReceived, name='orders'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
]
