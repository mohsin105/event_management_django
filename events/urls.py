from django.urls import path
from events.views import create_event,create_category,update_event,show_details,DeleteEvent
from users.views import dashboard
urlpatterns=[
    
    path('create-event/',create_event,name='create-event'),
    path('create-category/',create_category,name='create-category'),
    
    path('dashboard/',dashboard,name='dashboard'),
    path('update/<int:id>/',update_event,name='update-event'),
    path('details/<int:id>',show_details,name='details'),
    # path('details/<int:id>',EventDetails.as_view(),name='details'),
    # path('delete-event/<int:id>',delete_event,name='delete-event')
    path('delete-event/<int:id>',DeleteEvent.as_view(),name='delete-event')
]