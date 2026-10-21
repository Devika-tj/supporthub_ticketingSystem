from django.contrib import admin

from .models import (
    Department,
    RequestType,
    Ticket,
    TicketAttachment,
    TicketComment
)


admin.site.register(
    Department
)

admin.site.register(
    RequestType
)

admin.site.register(
    Ticket
)

admin.site.register(
    TicketAttachment
)

admin.site.register(
    TicketComment
)
