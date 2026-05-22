# Import the standard Django admin module to access administrative panel utilities.
from django.contrib import admin
# Import our custom Event and RSVP models from our events/models.py file.
from .models import Event, RSVP

# We create a customized configuration class for our Event model inside the admin interface.
# Think of this like arranging a specific dashboard layout so the shop owner can view and manage event listings.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # 'list_display' defines the columns that will be visible in the list view table of the admin panel.
    list_display = ('title', 'organizer', 'date', 'location')
    # 'search_fields' lets the admin search events by title or organizer email using a search box at the top.
    search_fields = ('title', 'organizer__email', 'location')
    # 'list_filter' adds a filtering sidebar on the right to easily filter events by date or organizer.
    list_filter = ('date', 'organizer')

# We create a customized configuration class for our RSVP guest list inside the admin interface.
# Think of this like creating an attendee ledger dashboard so we can track RSVPs at a glance.
@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    # 'list_display' defines the columns visible in the RSVP list view table.
    list_display = ('user', 'event', 'timestamp')
    # 'search_fields' lets the admin search RSVP logs by user email or event title.
    search_fields = ('user__email', 'event__title')
    # 'list_filter' adds a sidebar to filter RSVPs by event or registration date.
    list_filter = ('event', 'timestamp')
