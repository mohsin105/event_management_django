from django.urls import path
from users.views import create_participant,sign_in,sign_out,activate_user,assign_role,delete_participant,create_group,rsvp_to_events,group_list,admin_dashboard,show_participants,user_dashboard,rsvp_to_events
from events.views import show_dashboard
urlpatterns = [
    path('create-participant/',create_participant,name='create-participant'),
    path('sign-in/',sign_in,name='sign-in'),
    path('sign-out/',sign_out,name='sign-out'),
    path('activate/<int:user_id>/<str:token>/',activate_user),
    path('admin/<int:user_id>/assign-role/', assign_role,name='assign-role'),
    path('admin/create-group',create_group,name='create-group'),
    path('rsvp_events/<int:user_id>/<int:event_id>',rsvp_to_events,name='rsvp-events'),
    path('delete-event/<int:id>',delete_participant,name='delete-participant'),
    path('admin/group-list/',group_list,name='group-list'),
    path('admin/dashboard/',admin_dashboard,name='admin-dashboard'),
    path('admin/user-list/',show_participants,name='user-list'),
    path('organizer-dashboard/',show_dashboard,name='organizer-dashboard'),
    path('user-dashboard/',user_dashboard,name='user-dashboard'),
    path('rsvp-event/<int:event_id>',rsvp_to_events,name="rsvp-event")
]