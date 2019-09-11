from import_export import resources
from .models import Payment, Ticket


class PaymentResource(resources.ModelResource):
    class Meta:
        model = Payment


class TicketResource(resources.ModelResource):
    class Meta:
        model = Ticket
