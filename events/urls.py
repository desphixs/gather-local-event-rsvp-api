# Import the standard path utility from Django's URL routing engine.
from django.urls import path
# Import our custom EventListAPIView from our views.py file.
from .views import EventListAPIView

# We define a list of URL routing patterns for the events app.
# Think of this list like a roadsign map directing travelers to the correct room.
urlpatterns = [
    # We map the root empty path ('') to our EventListAPIView.
    # '.as_view()' is a Django method that converts our class-based view into a function the server can execute.
    # 'name="event-list"' assigns a nickname to this route so we can refer to it easily in our code.
    path('', EventListAPIView.as_view(), name='event-list'),
]
