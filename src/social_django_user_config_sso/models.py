from django.db import models

# Create your models here.

class UserDefinedSSOConfig(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="A unique name for this SSO configuration. Your SSO provider must send callbacks to /complete/'name'/ where 'name' is the name you enter here.")
    button_name = models.CharField(max_length=100, blank=True, help_text="A button label for the login page.")

    def __str__(self):
        return self.name

    def get_social_auth_settings(self):
        """
        Return a dictionary of settings for the social auth backend.
        This method should be overridden in subclasses to provide specific settings.
        """
        return {}

    def get_subclass_instance(self):
        """
        Introspects reverse relations to find and return the specific child instance.
        """
        # This could be replaced with 'django-model-utils' 'InheritanceManager'
        for relation in self._meta.related_objects:
            # Check if the relation is a subclass link via one-to-one inheritance
            if relation.parent_link:
                try:
                    # Access the lowercase attribute (e.g., parent_obj.childmodel)
                    return getattr(self, relation.get_accessor_name())
                except relation.related_model.DoesNotExist:
                    continue
                    
        # Return the original parent if no child subclass instance is found
        return self


class GitHubSSOConfig(UserDefinedSSOConfig):
    icon_class = 'fa-github'
    config_type = 'github'
    psa_backend_name = 'github'

    key = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)

    def get_social_auth_settings(self):
        return {
            "KEY": self.key,
            "SECRET": self.secret,
        }

class AzureADSSOConfig(UserDefinedSSOConfig):
    icon_class = 'fa-microsoft'
    config_type = 'azure'
    psa_backend_name = 'azuread-tenant-oauth2'

    client_id = models.CharField(max_length=255, help_text="Azure AD Application (Client) ID.")
    secret = models.CharField(max_length=255)
    tenant_id = models.CharField(max_length=255, blank=True, help_text="Azure AD Directory (Tenant) ID, leave blank for a multi-tenant app.")
    
    def get_social_auth_settings(self):
        kwargs = {
            "KEY": self.client_id,
            "SECRET": self.secret,
        }
        if self.tenant_id:
            kwargs["TENANT_ID"] = self.tenant_id
        return kwargs
