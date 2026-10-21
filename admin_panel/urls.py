from django.urls import path

from .views import (
    dashboard,
    create_user,
    users
)


app_name = 'admin_panel'


urlpatterns = [

    path(
        'dashboard/',
        dashboard,
        name='dashboard'
    ),

    path(
        'users/',
        users,
        name='users'
    ),

    path(
        'users/create/',
        create_user,
        name='create_user'
    ),
]