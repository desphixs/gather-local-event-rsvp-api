# Import the basic APIView class from Django REST Framework views.
from rest_framework.views import APIView
# Import the custom Response wrapper so we can return clean JSON formatting.
from rest_framework.response import Response
# Import the HTTP status codes bundle to return standardized API responses.
from rest_framework import status
# Import the standard Http404 exception helper from Django's HTTP module.
from django.http import Http404
# Import the Event model database table blueprint.
from .models import Event
# Import the EventSerializer to handle model-to-JSON translations.
from .serializers import EventSerializer

# The EventListAPIView handles HTTP GET and HTTP POST requests for our event feed list.
# Think of this view as a double-sided service desk:
# - GET: Allows anyone (visitors and logged-in users) to browse our list of meetup flyers.
# - POST: Allows only logged-in users to create and pin a brand-new meetup flyer on the board.
class EventListAPIView(APIView):
    
    # We define the GET method to handle event listings.
    # Anyone on the internet can hit this to browse active events.
    def get(self, request):
        # We query the database to retrieve all Event records in our table.
        # This returns a queryset list of Event objects.
        events = Event.objects.all()
        
        # We instantiate our EventSerializer, passing the events list.
        # 'many=True' tells the serializer that we are translating a list of events, not a single record!
        serializer = EventSerializer(events, many=True)
        
        # We return the translated JSON dictionary list with an HTTP 200 OK status code.
        return Response(serializer.data, status=status.HTTP_200_OK)

    # We define the POST method to handle event registrations.
    # Creating an event is restricted: we must make sure the organizer is logged in.
    def post(self, request):
        # We check if the user making the request is authenticated.
        # 'request.user.is_authenticated' is set by SimpleJWT when a valid bearer token is provided.
        if not request.user.is_authenticated:
            # If the user is anonymous, we immediately block them and return an error.
            # We return a 401 Unauthorized status, telling them they need to log in first!
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        # If they are logged in, we feed the raw request body data into our EventSerializer customs check.
        serializer = EventSerializer(data=request.data)
        
        # We run our serializer field validations.
        # This checks if the title exists, location isn't empty, and the date is a valid format.
        if serializer.is_valid():
            # If the data is valid, we save the new event record in the database.
            # Crucial security step: we inject 'organizer=request.user' inside .save()!
            # Since organizer is read-only, this forces the host to be the user who is logged in,
            # preventing any malicious users from pretending to host events for someone else!
            serializer.save(organizer=request.user)
            
            # We return the newly created event data with a friendly HTTP 201 Created status.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        # If validations fail, we return the error dictionary with an HTTP 400 Bad Request status.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# The EventDetailAPIView handles HTTP GET, PUT, and DELETE requests for a single event.
# Think of this view like a specialized security vault:
# - GET: Anyone can peek through the glass box and view a specific event's details.
# - PUT: Allows ONLY the original organizer of the event to edit its details.
# - DELETE: Allows ONLY the original organizer of the event to delete it from the system.
class EventDetailAPIView(APIView):
    
    # A helper method to fetch a single event by its ID.
    # Think of this like a helper looking up an item code in the inventory system.
    def get_object(self, event_id):
        # We start a try-except block to safely capture errors if the database lookup fails.
        try:
            # We search our Event table for a record with the matching event_id (primary key).
            return Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            # If no event is found with that ID, we raise a Http404 exception.
            # Django REST Framework will catch this exception and automatically convert it
            # into a clean 404 Not Found JSON error response!
            raise Http404

    # GET method to fetch details for a single specific event.
    def get(self, request, event_id):
        # We call our helper method to fetch the event. If not found, a 404 is automatically returned.
        event = self.get_object(event_id)
        
        # We pass the single database event record to our EventSerializer translator.
        # Since we are serializing a single record, we do NOT pass many=True!
        serializer = EventSerializer(event)
        
        # We return the translated event JSON payload with a success HTTP 200 OK status.
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT method to update a single event's details.
    def put(self, request, event_id):
        # We call our helper method to fetch the event record from the database.
        event = self.get_object(event_id)
        
        # Security Bouncer Check: Make sure the user making the request is authenticated!
        if not request.user.is_authenticated:
            # If anonymous, we block them immediately and return a 401 Unauthorized status.
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        # Object-Level Permission Check: Verify if the user is the original host/organizer.
        # If the logged-in user (request.user) does not match the event's organizer, we block them!
        if event.organizer != request.user:
            # If they don't match, we return an HTTP 403 Forbidden status.
            # This is our critical guard preventing people from changing other users' events!
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # We pass the existing database record and the incoming request payload data into our serializer.
        # Passing both targets the existing record to perform an UPDATE instead of a new INSERT!
        serializer = EventSerializer(event, data=request.data)
        
        # We validate the incoming update data fields.
        if serializer.is_valid():
            # If valid, we save the updates to our database table.
            serializer.save()
            # We return the updated data back with a success HTTP 200 OK status.
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        # If validations fail, we return the error dictionary with an HTTP 400 Bad Request status.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method to remove a single event from the database.
    def delete(self, request, event_id):
        # We call our helper method to fetch the event record.
        event = self.get_object(event_id)
        
        # Security Bouncer Check: Make sure the user is logged in.
        if not request.user.is_authenticated:
            # If they aren't logged in, block them with a 401 Unauthorized status.
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        # Object-Level Permission Check: Only the organizer is allowed to delete this event!
        if event.organizer != request.user:
            # If they don't match, block them with a 403 Forbidden status.
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # If they pass all checks, we call .delete() to remove the record permanently from the table.
        event.delete()
        
        # We return a response with an HTTP 204 No Content status, which means the deletion was highly successful!
        return Response(status=status.HTTP_204_NO_CONTENT)
