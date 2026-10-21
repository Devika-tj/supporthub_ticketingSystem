from django.urls import path

from .views import dashboard


app_name = 'support_staff'


urlpatterns = [

    path(
        'dashboard/',
        dashboard,
        name='dashboard'
    ),
]