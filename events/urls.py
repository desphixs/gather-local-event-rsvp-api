# Import the standard path utility from Django's URL routing engine.
from django.urls import path
# Import our custom views from our views.py file.
# We also import RSVPAPIView here so that the routing engine knows about our new RSVP join/cancel desk!
from .views import EventListAPIView, EventDetailAPIView, RSVPAPIView

# We define a list of URL routing patterns for the events app.
# Think of this list like a roadsign map directing travelers to the correct room.
urlpatterns = [
    # We map the root empty path ('') to our EventListAPIView.
    # '.as_view()' is a Django method that converts our class-based view into a function the server can execute.
    # 'name="event-list"' assigns a nickname to this route so we can refer to it easily in our code.
    path('', EventListAPIView.as_view(), name='event-list'),
    
    # We map the detail path containing a dynamic integer parameter ('<int:event_id>/') to our EventDetailAPIView.
    # '<int:event_id>' tells Django to capture whatever integer is passed in the URL (like /api/events/3/)
    # and pass it as the keyword argument 'event_id' straight into our view methods!
    # 'name="event-detail"' assigns a nickname to this specific route for future reverse lookups.
    path('<int:event_id>/', EventDetailAPIView.as_view(), name='event-detail'),
    
    # We map the RSVP endpoint route with the dynamic parameter: '<int:event_id>/rsvp/'.
    # This route captures the ID of the event and routes any HTTP requests to the RSVPAPIView.
    # Just like the other routes, we call '.as_view()' to make the class compatible with Django's URL matcher.
    # We assign the name 'event-rsvp' as a clear nickname so that other parts of our app can build RSVP URLs dynamically.
    path('<int:event_id>/rsvp/', RSVPAPIView.as_view(), name='event-rsvp'),
]
