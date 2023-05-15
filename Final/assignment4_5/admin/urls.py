from django.urls import path
from . import views


urlpatterns = [
    path('', views.AdminPanel, name='admin'),
    path('create', views.CreateProduct.as_view(), name='create'),
    path('update/<int:pk>', views.UpdateProduct, name='update'),
    path('delete/<int:pk>', views.DeleteProduct, name='delete'),

    path('check_users', views.CheckUsers.as_view(), name='check_users'),
    path('user/<int:pk>', views.DetailUser.as_view(), name='detail_user'),

    path('user/delete/<int:pk>', views.DeleteUser.as_view(), name='delete_user'),
    path('user/edit-profile/<int:pk>', views.EditUserProfile.as_view(), name='edit_user_profile'),
]