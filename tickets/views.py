from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)


from .forms import (
    TicketCommentForm,
    TicketForm
)

from .models import (
    RequestType,
    Ticket,
    TicketAttachment
)


@login_required
def my_tickets(request):

    tickets = (
        Ticket.objects
        .filter(
            created_by=request.user
        )
        .select_related(
            'department',
            'request_type'
        )
    )


    status = request.GET.get(
        'status',
        'all'
    )


    query = request.GET.get(
        'q',
        ''
    ).strip()


    if status in {
        'open',
        'in_progress',
        'resolved'
    }:

        tickets = tickets.filter(
            status=status
        )


    if query:

        tickets = (
            tickets.filter(
                title__icontains=query
            )
            |
            tickets.filter(
                ticket_no__icontains=query
            )
        )


    return render(
        request,
        'tickets/my_tickets.html',
        {
            'tickets': tickets,
            'active_status': status,
            'query': query
        }
    )


@login_required
def create_ticket(request):

    if request.method == 'POST':

        form = TicketForm(
            request.POST,
            request.FILES
        )


        if form.is_valid():

            ticket = form.save(
                commit=False
            )


            ticket.created_by = request.user

            ticket.save()


            for f in request.FILES.getlist(
                'attachments'
            ):

                TicketAttachment.objects.create(
                    ticket=ticket,
                    file=f
                )


            messages.success(
                request,
                'Ticket created successfully!'
            )


            return redirect(
                'tickets:detail',
                ticket_no=ticket.ticket_no
            )


    else:

        form = TicketForm()


    return render(
        request,
        'tickets/create.html',
        {
            'form': form
        }
    )


@login_required
def request_types_api(request):

    department_id = request.GET.get(
        'department'
    )


    rows = (
        RequestType.objects
        .filter(
            department_id=department_id,
            is_active=True
        )
        .values(
            'id',
            'name'
        )
        if department_id
        else []
    )


    return JsonResponse(
        list(rows),
        safe=False
    )


@login_required
def ticket_detail(
    request,
    ticket_no
):

    ticket = get_object_or_404(

        Ticket.objects
        .select_related(
            'department',
            'request_type',
            'created_by',
            'assigned_to'
        )
        .prefetch_related(
            'attachments',
            'comments__author'
        ),

        ticket_no=ticket_no,

        created_by=request.user
    )


    if request.method == 'POST':

        form = TicketCommentForm(
            request.POST
        )


        if form.is_valid():

            c = form.save(
                commit=False
            )


            c.ticket = ticket

            c.author = request.user

            c.save()


            return redirect(
                'tickets:detail',
                ticket_no=ticket.ticket_no
            )


    else:

        form = TicketCommentForm()


    return render(
        request,
        'tickets/detail.html',
        {
            'ticket': ticket,
            'comment_form': form
        }
    )