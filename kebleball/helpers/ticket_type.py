# coding: utf-8
"""Model for a ticket type."""

from __future__ import unicode_literals

import collections

_TicketType = collections.namedtuple(
    "TicketType",
    [
        "name",
        "slug",
        "price",
        "limit_per_person",
        "total_limit",
        "counts_towards_guest_limit",
        "can_buy",
    ]
)


class TicketType(_TicketType):
    """Namedtuple model for ticket types.

    Attributes:
        name: (str) Human readable name for the ticket type.
        slug: (str) Machine readable slug for the ticket type.
        price: (int) Price for the ticket in pence.
        limit_per_person: (int) Maximum number of this type of ticket any one
            person can buy. -1 if unlimited
        total_limit: (int) Maximum number of tickets of this type that can be
            bought. -1 if unlimited
        counts_towards_guest_limit: (bool) whether tickets of this type count
            towards the overall limit on number of guests.
        can_buy: (function(database.user.User): bool) routine which determines
             whether the given user can buy/create tickets of this type through
             the main purchase flow.
    """
