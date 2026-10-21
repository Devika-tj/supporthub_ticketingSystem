from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.shortcuts import (
    redirect,
    render
)

from login.forms import CreateUserForm

from login.models import User


def admin_only(view):

    def wrapper(
        request,
        *args,
        **kwargs
    ):

        if not request.user.is_authenticated:

            return redirect(
                'login:login_page'
            )


        if (
            request.user.role != 'admin'
            and not request.user.is_superuser
        ):

            return redirect(
                'tickets:my_tickets'
            )


        return view(
            request,
            *args,
            **kwargs
        )


    return wrapper


@admin_only
def dashboard(request):

    context = {

        'total_users':
            User.objects
            .exclude(
                role='admin'
            )
            .count(),

        'staff_count':
            User.objects
            .filter(
                role='staff'
            )
            .count(),

        'support_count':
            User.objects
            .filter(
                role='support'
            )
            .count(),
    }


    return render(
        request,
        'admin_app/dashboard.html',
        context
    )


@admin_only
def create_user(request):

    if request.method == 'POST':

        form = CreateUserForm(
            request.POST
        )


        if form.is_valid():

            user = form.save()


            messages.success(
                request,
                f'{user.get_role_display()} account '
                f'{user.username} created successfully.'
            )


            return redirect(
                'admin_app:users'
            )


    else:

        form = CreateUserForm()


    return render(
        request,
        'admin_app/create_user.html',
        {
            'form': form
        }
    )


@admin_only
def users(request):

    return render(
        request,
        'admin_app/users.html',
        {
            'users':
                User.objects
                .exclude(
                    role='admin'
                )
                .order_by(
                    '-date_joined'
                )
        }
    )
