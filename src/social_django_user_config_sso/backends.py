
from social_core.backends.base import BaseAuth

class UserDefinedOAuthMixin(BaseAuth):
    def __init__(self, defined_settings={}, strategy=None, redirect_uri=None):
        self.defined_settings = defined_settings
        for setting_name, setting_value in defined_settings.items():
            setattr(self, setting_name, setting_value)
        super().__init__(strategy, redirect_uri)


from social_core.backends.github import GithubOAuth2
class UserDefinedGithubOAuth2(UserDefinedOAuthMixin, GithubOAuth2):
    DEFAULT_SCOPE  = ['user:email']


# The tenant backend reads TENANT_ID, AzureADOAuth2 always uses the common endpoint
from social_core.backends.azuread_tenant import AzureADTenantOAuth2
class UserDefinedAzureADOAuth2(UserDefinedOAuthMixin, AzureADTenantOAuth2):
    pass
