from django.urls import path

from .views import (
    UserLoginView,
    UserLogoutView
)


app_name = 'login'


urlpatterns = [

    path(
        '',
        UserLoginView.as_view(),
        name='login'
    ),

    path(
        'login/',
        UserLoginView.as_view(),
        name='login_page'
    ),

    path(
        'logout/',
        UserLogoutView.as_view(),
        name='logout'
    ),
]