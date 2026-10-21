from django.contrib.auth.decorators import login_required

from django.shortcuts import render

from tickets.models import Ticket


@login_required
def dashboard(request):

    if request.user.role != 'support':

        return render(
            request,
            'support_staff/not_allowed.html',
            status=403
        )


    context = {

        'open_count':
            Ticket.objects.filter(
                status='open'
            ).count(),

        'progress_count':
            Ticket.objects.filter(
                status='in_progress'
            ).count(),

        'resolved_count':
            Ticket.objects.filter(
                status='resolved'
            ).count(),

        'tickets':
            Ticket.objects
            .select_related(
                'created_by',
                'department',
                'request_type'
            )[:10],
    }


    return render(
        request,
        'support_staff/dashboard.html',
        context
    )