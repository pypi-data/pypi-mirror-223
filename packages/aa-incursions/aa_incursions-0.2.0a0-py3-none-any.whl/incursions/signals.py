import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from incursions.models import Incursion
from incursions.tasks import (
    incursion_ended, incursion_established, incursion_mobilizing,
    incursion_withdrawing,
)

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Incursion)
def incursion(sender, instance: Incursion, created: bool, *args, **kwargs):
    update_fields = kwargs.pop('update_fields', []) or []
    if created is True:
        incursion_established.apply_async(args=[instance.pk])
    elif 'state' not in update_fields:
        return
    else:
        if instance.state == Incursion.States.ESTABLISHED:
            # This should have been handled above?
            return
        if instance.state == Incursion.States.MOBILIZING:
            incursion_mobilizing.apply_async(args=[instance.pk])
            return
        if instance.state == Incursion.States.WITHDRAWING:
            incursion_withdrawing.apply_async(args=[instance.pk])
            return
        if instance.state == Incursion.States.ENDED:
            incursion_ended.apply_async(args=[instance.pk])
            return
