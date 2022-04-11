# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.signals import setting_changed
# from django.apps import apps
# from django.contrib import contenttypes
#
#
# @receiver(setting_changed)
# def user_model_swapped(**kwargs):
#     if kwargs["setting"] == "AUTH_USER_MODEL":
#         apps.clear_cache()
#
#
# @receiver(setting_changed)
# def user_model_swapped_changed(**kwargs):
#     if kwargs['setting'] == 'AUTH_USER_MODEL':
#         apps.clear_cache()
#
#
# def post_save_receiver(sender, instance, created, **kwargs):
#     pass
#
#
# post_save.connect(post_save_receiver, sender=settings.AUTH_USER_MODEL)
