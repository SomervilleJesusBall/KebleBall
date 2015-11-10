# coding: utf-8
"""Various business logic functions for the purchase flow."""

from kebleball import app
from kebleball.database import models

def get_ticket_limit(user, ticket_type):
    """Get the number of tickets of |type| that |user| can purchase.

    Args:
        user: (models.User) The user purchasing tickets.
        ticket_type: (kebleball.helpers.ticket_type.TicketType) the type of
            ticket being purchased

    Returns:
        (int) the number of |ticket_type| tickets that |user| can buy.
    """

    limit = min(
        ticket_type.limit_per_person - user.tickets.filter(
            models.Ticket.ticket_type == ticket_type.slug and
            models.Ticket.cancelled == False
        ).count(),
        ticket_type.total_limit - models.Ticket.query.filter(
            models.Ticket.ticket_type == ticket_type.slug and
            models.Ticket.cancelled == False
        ).count(),
        app.APP.config['MAX_TICKETS'] - user.tickets.filter(
            models.Ticket.cancelled == False
        ).count(),
        app.APP.config['MAX_TICKETS_PER_TRANSACTION']
    )

    if ticket_type.counts_towards_guest_limit:
        limit = min(
            limit,
            app.APP.config[
                'GUEST_TICKETS_AVAILABLE'] - models.Ticket.query.filter(
                models.Ticket.ticket_type in app.APP.config[
                    'GUEST_TYPE_SLUGS'] and
                models.Ticket.cancelled == False
            ).count()
        )

    return max(0, limit)

def get_available_ticket_types(user):
    available_types = []

    for ticket_type in app.APP.config['TICKET_TYPES']:
        if ticket_type.can_buy(user):
            ticket_limit = get_ticket_limit(user, ticket_type)

            if ticket_limit > 0:
                available_types.append((ticket_type, ticket_limit))
