from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.HomePage.as_view(), name='home-page'),
    path('Contacs/', views.Contacs, name='Contacs'),
    path('product/<int:pk>', views.ProductDetail.as_view(), name='product-detail'),
		path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
]
