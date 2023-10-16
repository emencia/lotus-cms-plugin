from django.apps import apps
from django.conf import settings


def safe_get_user_model():
    """
    Safe loading of the User model, customized or not.
    """
    user_app, user_model = settings.AUTH_USER_MODEL.split(".")
    return apps.get_registered_model(user_app, user_model)
