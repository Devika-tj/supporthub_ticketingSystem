from django.contrib import messages

from django.contrib.auth import (
    update_session_auth_hash
)

from django.contrib.auth.decorators import login_required

from django.shortcuts import (
    redirect,
    render
)

from .forms import (
    SupportHubPasswordChangeForm
)


@login_required
def profile(request):

    return render(
        request,
        'staff_portal/profile.html'
    )


@login_required
def change_password(request):

    if request.method == 'POST':

        form = SupportHubPasswordChangeForm(
            request.user,
            request.POST
        )


        if form.is_valid():

            user = form.save()


            update_session_auth_hash(
                request,
                user
            )


            messages.success(
                request,
                'Password changed successfully.'
            )


            return redirect(
                'staff_portal:profile'
            )


    else:

        form = SupportHubPasswordChangeForm(
            request.user
        )


    return render(
        request,
        'staff_portal/change_password.html',
        {
            'form': form
        }
    )