# Import the basic APIView class from Django REST Framework views.
from rest_framework.views import APIView
# Import the custom Response wrapper so we can return clean JSON formatting.
from rest_framework.response import Response
# Import the HTTP status codes bundle to return standardized API responses.
from rest_framework import status
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
