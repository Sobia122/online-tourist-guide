from django.db.models.signals import post_save
from django.dispatch import receiver
from destinations.models import Activity, TravelTip
from users.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

# Activity Notification
@receiver(post_save, sender=Activity)
def notify_new_activity(sender, instance, created, **kwargs):
    if created:
        for user in User.objects.all():
            Notification.objects.create(
                user=user,
                message=f"🎯 New activity '{instance.title}' added! Check it out."
            )

# TravelTip Notification
@receiver(post_save, sender=TravelTip)
def notify_new_tip(sender, instance, created, **kwargs):
    if created:
        for user in User.objects.all():
            Notification.objects.create(
                user=user,
                message=f"🧳 New travel tip: {instance.title}"
            )
