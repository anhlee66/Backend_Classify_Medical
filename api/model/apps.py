from django.apps import AppConfig


class ModelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.model"
    label = "api_label"
