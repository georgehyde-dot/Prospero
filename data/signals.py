from .models import APIMethod, APIMethodModifier
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# create a signal that saves search values
# @receiver(post_save, sender=User)
# def post_save_search_values(sender, instance, created, **kwargs):
#   ...

# create a signal that saves search results 
# @receiver(post_save, sender=User)
# def post_save_search_results(sender, instance, created, **kwargs):
#   ...