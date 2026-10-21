from django.conf import settings

from django.db import models


class Department(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )


    is_active = models.BooleanField(
        default=True
    )


    class Meta:

        ordering = ['name']


    def __str__(self):

        return self.name


class RequestType(models.Model):

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='request_types'
    )


    name = models.CharField(
        max_length=150
    )


    is_active = models.BooleanField(
        default=True
    )


    class Meta:

        ordering = ['name']


        constraints = [
            models.UniqueConstraint(
                fields=[
                    'department',
                    'name'
                ],
                name='unique_request_per_department'
            )
        ]


    def __str__(self):

        return self.name


class Ticket(models.Model):

    STATUS_CHOICES = [

        (
            'open',
            'Open'
        ),

        (
            'in_progress',
            'In Progress'
        ),

        (
            'resolved',
            'Resolved'
        ),
    ]


    PRIORITY_CHOICES = [

        (
            'low',
            'Low'
        ),

        (
            'medium',
            'Medium'
        ),

        (
            'high',
            'High'
        ),
    ]


    ticket_no = models.PositiveIntegerField(
        unique=True,
        editable=False,
        null=True
    )


    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets'
    )


    title = models.CharField(
        max_length=200
    )


    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='tickets'
    )


    request_type = models.ForeignKey(
        RequestType,
        on_delete=models.PROTECT,
        related_name='tickets'
    )


    other_request = models.CharField(
        max_length=255,
        blank=True
    )


    remarks = models.TextField(
        blank=True
    )


    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='open'
    )


    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
    )


    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets',
        limit_choices_to={
            'role': 'support'
        }
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:

        ordering = [
            '-created_at'
        ]


    def save(self, *args, **kwargs):

        if self.ticket_no is None:

            last = Ticket.objects.order_by(
                '-ticket_no'
            ).first()


            self.ticket_no = (
                last.ticket_no + 1
                if last and last.ticket_no
                else 1
            )


        super().save(
            *args,
            **kwargs
        )


    def __str__(self):

        return f'TICKET-{self.ticket_no}'


class TicketAttachment(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='attachments'
    )


    file = models.FileField(
        upload_to='ticket_attachments/%Y/%m/'
    )


    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )


class TicketComment(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='comments'
    )


    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )


    comment = models.TextField()


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:

        ordering = [
            'created_at'
        ]