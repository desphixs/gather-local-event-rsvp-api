# Import the core serializers class from the Django REST Framework package.
from rest_framework import serializers
# Import our Event and RSVP models from events/models.py to bind them to our serializers.
from events.models import Event, RSVP

# The EventSerializer handles translation between Event Python objects and JSON format.
# Think of it like a Customs Officer at an international border:
# - Incoming: It validates the user's input (checks if location is valid, date is correct) before saving.
# - Outgoing: It formats the database record into neat JSON text so frontends can display it.
class EventSerializer(serializers.ModelSerializer):
    # We define the organizer field explicitly as a read-only field.
    # We serialize the organizer's primary key (ID) but make sure users cannot submit their own organizer ID.
    # The server will automatically assign the logged-in user as the organizer for safety!
    organizer = serializers.PrimaryKeyRelatedField(
        read_only=True,
        help_text="The ID of the user hosting this event (automatically set by server)."
    )

    # The Meta class defines configuration blueprints for this ModelSerializer.
    class Meta:
        # We bind this serializer class to our Event database model table.
        model = Event
        # We instruct the serializer to expose all columns/fields from our Event model in the JSON payload.
        fields = '__all__'
        # 'read_only_fields' acts as an extra security list.
        # It guarantees that even if a user tries to send an 'organizer' field in a POST request,
        # Django REST Framework will discard it and protect our event hosts from identity spoofing.
        read_only_fields = ['organizer']


# The RSVPSerializer handles translation between RSVP Python records and JSON format.
# Think of it like a guestlist registrar that translates attendee registrations into neat digital data cards.
class RSVPSerializer(serializers.ModelSerializer):
    # We define the user field explicitly as a read-only field.
    # A user shouldn't be able to type in another person's user ID to RSVP for them!
    # The server will automatically bind the current logged-in request.user as the attendee.
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        help_text="The ID of the attendee (automatically set to the logged-in user)."
    )

    # The Meta class defines configurations for our RSVP ModelSerializer.
    class Meta:
        # We bind this serializer directly to our RSVP model Guestlist table.
        model = RSVP
        # We expose all fields: id, user, event, and timestamp.
        fields = '__all__'
        # We mark 'user' as read-only inside the Meta settings to lock down registrations.
        # This acts as our second line of defense to prevent users from RSVPing on behalf of others.
        read_only_fields = ['user']
