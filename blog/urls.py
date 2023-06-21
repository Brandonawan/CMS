from django.urls import path
# from .views import
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('add_post/', add_post, name='add_post'),
    path('post_detail/<int:post_id>/', post_detail, name='post_detail'),
    path('edit_post/<int:post_id>/', edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('check_username_availability/', check_username_availability, name='check_username_availability'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]