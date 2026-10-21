from django.urls import path

from .views import (
    change_password,
    profile
)


app_name = 'staff_portal'


urlpatterns = [

    path(
        '',
        profile,
        name='profile'
    ),

    path(
        'change-password/',
        change_password,
        name='change_password'
    ),
]