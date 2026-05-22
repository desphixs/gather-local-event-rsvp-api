# Import the core Django models module to access base model blueprints.
from django.db import models
# Import settings from django.conf to dynamically refer to our custom User model.
from django.conf import settings

# The Event model represents a scheduled meetup hosted by an organizer.
# Think of it like creating a blueprint for an event flyer that has a title, description, location, date, and host.
class Event(models.Model):
    # 'title' stores the name of the event (e.g. "Python for Beginners").
    # CharField is used for short text strings, and max_length limits it to 200 characters.
    title = models.CharField(
        max_length=200,
        help_text="The title of the local meetup or event."
    )
    
    # 'description' stores a detailed paragraph explaining what the event is about.
    # TextField is designed for longer, multi-line blocks of text.
    description = models.TextField(
        blank=True,
        help_text="A detailed description of what will happen at the meetup."
    )
    
    # 'location' stores where the meetup is happening (e.g. "Central Park Coffee Shop").
    # CharField is ideal here since addresses or names of venues are typically short.
    location = models.CharField(
        max_length=255,
        help_text="The physical venue or address where the event will take place."
    )
    
    # 'date' stores the date and time when the event will start.
    # DateTimeField stores both the calendar date and the exact clock time.
    date = models.DateTimeField(
        help_text="The scheduled date and time for this event."
    )
    
    # 'organizer' links this event to the User who created it.
    # ForeignKey creates a one-to-many relationship: one user can organize many events.
    # 'settings.AUTH_USER_MODEL' dynamically fetches our custom User model (accounts.User).
    # 'on_delete=models.CASCADE' means if the User is deleted, all their organized events are also deleted.
    # 'related_name="events"' lets us easily lookup a user's events via 'user.events.all()'.
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events',
        help_text="The host or creator of the event."
    )

    # The __str__ method defines the human-readable string representation of this object.
    # Instead of showing "Event Object (1)" in administrative panels, it will show the actual title.
    def __str__(self):
        # Return the title string directly
        return self.title


# The RSVP model tracks who is attending which event.
# Think of it like a sign-up sheet or guestlist. Each row links one User to one Event.
class RSVP(models.Model):
    # 'user' links this sign-up sheet entry to a registered User.
    # ForeignKey creates a link to the User model.
    # 'on_delete=models.CASCADE' means if the user deletes their account, their RSVPs are cleaned up.
    # 'related_name="rsvps"' lets us see all RSVPs a user has made via 'user.rsvps.all()'.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rsvps',
        help_text="The user who is RSVPing to the event."
    )
    
    # 'event' links this sign-up sheet entry to a specific Event.
    # ForeignKey creates a link to our Event model.
    # 'on_delete=models.CASCADE' means if the event is deleted, all RSVPs to it are also deleted.
    # 'related_name="rsvps"' lets us see all RSVPs for an event via 'event.rsvps.all()'.
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='rsvps',
        help_text="The event the user is attending."
    )
    
    # 'timestamp' records exactly when the user signed up or RSVP'd.
    # 'auto_now_add=True' tells Django to automatically grab the current clock time when the record is created.
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="The exact time when this RSVP was submitted."
    )

    # The Meta class defines extra configuration options for our model.
    class Meta:
        # 'unique_together' is a constraint that ensures a user cannot sign up for the same event multiple times.
        # This acts like a security guard checking the guestlist so a person's name isn't written down twice!
        unique_together = ['user', 'event']

    # The __str__ method defines the human-readable string representation of this RSVP record.
    # It shows who RSVP'd to what, making administrative viewing clean and readable.
    def __str__(self):
        # Return a formatted string combining user email and event title
        return f"{self.user.email} RSVP'd to {self.event.title}"
