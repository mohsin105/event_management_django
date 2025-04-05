from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth import get_user_model

User=get_user_model()

# @receiver(post_save, sender=User)
# def send_activation_email(sender, instance, created, **kwargs):
#     if created:
#         token = default_token_generator.make_token(instance)
#         activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"

#         subject = 'Activate Your Account'
#         message = f"Hi {instance.username},Please activate your account by clicking the link below: {activation_url} Thank You!"
#         recipient_list = [instance.email]

#         try:
#             send_mail(subject, message,
#                       'mohsinibnaftab@gmail.com', recipient_list)
#         except Exception as e:
#             print(f"Failed to send email to {instance.email}: {str(e)}")

# Assign default role to new registered person
@receiver(post_save,sender=User)
def assign_role(sender,instance,created,**kwargs):
    if created:
        participant_group,created=Group.objects.get_or_create(name='Participant')
        instance.groups.add(participant_group)
        instance.save()

# @receiver(m2m_changed,sender=User.rsvp_events.through)
# def notify_event_rsvp(sender,instance,action,**kwargs):
#     if action == 'post_add':
#         print(instance, instance.participants.all())

#         assigned_emails = [user.email for user in instance.participants.all()]
#         print("Checking....", assigned_emails)

#         send_mail(
#             "New Event Assigned",
#             f"You have been assigned to the event",
#             settings.EMAIL_HOST_USER,
#             assigned_emails,
#             fail_silently=False,
#         )