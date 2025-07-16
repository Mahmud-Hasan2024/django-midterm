from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from events.models import Event

User = get_user_model()


@receiver(m2m_changed, sender=Event.participants.through)
def send_rsvp_email(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            user = User.objects.get(pk=user_id)
            send_mail(
                subject="RSVP Confirmation",
                message=f"Hi {user.username}, you've successfully RSVPed to the event '{instance.name}'.",
                from_email="lboy71943@gmail.com",
                recipient_list=[user.email],
                fail_silently=False,
            )