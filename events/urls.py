from django.urls import path
from events.views import create_event,create_category,show_dashboard,update_event,show_details,delete_event
from users.views import dashboard
urlpatterns=[
    
    path('create-event/',create_event,name='create-event'),
    path('create-category/',create_category,name='create-category'),
    
    path('dashboard/',dashboard,name='dashboard'),
    path('update/<int:id>/',update_event,name='update-event'),
    path('details/<int:id>',show_details,name='details'),
    path('delete-event/<int:id>',delete_event,name='delete-event')
]