from django.db.models.signals import post_save
from django.dispatch import receiver
from tourismo.models import Plan, GuideRequest

@receiver(post_save, sender=GuideRequest)
def update_plan_status(sender, instance, **kwargs):
    if instance.accepted:
        plan = instance.plan
        plan.status = 'expired'
        plan.save()

