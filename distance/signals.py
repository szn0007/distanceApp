# signals.py
from django.contrib.postgres.search import SearchVector
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Location

@receiver(post_save, sender=Location)
def update_search_vector(sender, instance, created, **kwargs):
    if created:
        instance.search_vector = (
            SearchVector('name', weight='A') +
            SearchVector('address', weight='B')
        )
        instance.save(update_fields=['search_vector'])
