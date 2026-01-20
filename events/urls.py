from django.urls import path
from events.views import create_event,create_category,show_details,DeleteEvent, UpdateCategory, EventList, UpdateEvent
from users.views import dashboard
urlpatterns=[
    
    path('create-event/',create_event,name='create-event'),
    path('create-category/',create_category,name='create-category'),
    path('update-category/<int:category_id>/',UpdateCategory.as_view(), name='update-category'),
    path('', EventList.as_view(), name='events'),
    path('dashboard/',dashboard,name='dashboard'),
    path('update/<int:id>/',UpdateEvent.as_view(),name='update-event'),
    path('details/<int:id>',show_details,name='details'),
    # path('details/<int:id>',EventDetails.as_view(),name='details'),
    # path('delete-event/<int:id>',delete_event,name='delete-event')
    path('delete-event/<int:id>',DeleteEvent.as_view(),name='delete-event')
]