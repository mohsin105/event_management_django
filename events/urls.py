from django.urls import path
from events.views import details
urlpatterns=[
    path('details/',details)
]