from django.apps import AppConfig


class SocialDjangoUserConfigSsoConfig(AppConfig):
    name = "social_django_user_config_sso"
    # Matches the existing migration, django < 6 defaults this to AutoField
    default_auto_field = "django.db.models.BigAutoField"
