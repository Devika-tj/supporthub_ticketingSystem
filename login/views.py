from django.contrib.auth.views import (
    LoginView,
    LogoutView
)

from .forms import LoginForm


class UserLoginView(LoginView):

    template_name = 'login/login.html'

    authentication_form = LoginForm

    redirect_authenticated_user = True


    def get_success_url(self):

        role = self.request.user.role


        if role == 'support':

            return '/support/dashboard/'


        if role == 'admin':

            return '/admin-panel/dashboard/'


        return '/tickets/'


class UserLogoutView(LogoutView):

    next_page = '/login/'
