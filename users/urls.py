from django.urls import path
from users.views import create_participant,sign_in,sign_out,activate_user,assign_role,delete_participant,create_group,rsvp_to_events,admin_dashboard,show_participants,user_dashboard,rsvp_to_events,GroupList,ProfileView,UpdateProfile, ChangePassword, CustomPasswordResetView, CustomPasswordResetConfirmView,UpdateGroup,delete_group,OrganizerDashboard, AdminEventList
from events.views import DeleteCategory,CategoryList
from django.contrib.auth.views import  PasswordChangeDoneView


urlpatterns = [
    path('create-participant/',create_participant,name='create-participant'),
    path('sign-in/',sign_in,name='sign-in'),
    path('sign-out/',sign_out,name='sign-out'),
    path('activate/<int:user_id>/<str:token>/',activate_user),
    path('admin/<int:user_id>/assign-role/', assign_role,name='assign-role'),
    path('admin/create-group',create_group,name='create-group'),
    path('rsvp_events/<int:user_id>/<int:event_id>',rsvp_to_events,name='rsvp-events'),
    path('delete-event/<int:id>',delete_participant,name='delete-participant'),
    path('admin/event-list/',AdminEventList.as_view(),name='admin-event-list'),
    path('admin/group-list/',GroupList.as_view(),name='group-list'),
    path('admin/update-group/<int:group_id>/',UpdateGroup.as_view(), name='update-group'),
    path('admin/delete-group/<int:group_id>/', delete_group, name='delete-group'),
    path('admin/dashboard/',admin_dashboard,name='admin-dashboard'),
    path('admin/user-list/',show_participants,name='user-list'),
    
    path('organizer-dashboard/',OrganizerDashboard.as_view(),name='organizer-dashboard'),
    path('user-dashboard/',user_dashboard,name='user-dashboard'),
    path('rsvp-event/<int:event_id>',rsvp_to_events,name="rsvp-event"),
    path('admin/category-list/',CategoryList.as_view(),name='category-list'),
    path('delete-category/<int:id>/',DeleteCategory.as_view(),name='delete-category'),
    path('user-profile/',ProfileView.as_view(),name='user-profile'),
    path('update-profile/<int:id>/',UpdateProfile.as_view(),name='update-profile'),
    path('password-change/', ChangePassword.as_view(),name='password-change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password-reset'),
    path('password-reset/confirm/<uidb64>/<token>/',CustomPasswordResetConfirmView.as_view(),name='password_reset_confirm')
]


# path('organizer-dashboard/',show_dashboard,name='organizer-dashboard'),
# path('admin/group-list/',group_list,name='group-list'),