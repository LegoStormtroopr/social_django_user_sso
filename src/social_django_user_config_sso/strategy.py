from social_core.backends.base import BaseAuth
from social_django.strategy import DjangoStrategy

class UserDefinedDjangoStrategy(DjangoStrategy):
    def setting(self, name: str, default=None, backend: BaseAuth | None = None):
        from social_core.strategy import setting_name

        if backend and hasattr(backend, 'defined_settings') and name in backend.defined_settings.keys():
            value = backend.defined_settings.get(name, default)
            return value

        return super().setting(name, default, backend)

    def get_backend(
        self, name: str, redirect_uri: str | None = None, **kwargs
    ) -> BaseAuth:
        """Return a configured backend instance"""
        
        from django.shortcuts import get_object_or_404
        from .models import UserDefinedSSOConfig

        backend_obj = get_object_or_404(UserDefinedSSOConfig, name=name).get_subclass_instance()
        backend_name = backend_obj.psa_backend_name
        user_settings = backend_obj.get_social_auth_settings()
        
        backend_class = self.get_backend_class(backend_name)
        kwargs["redirect_uri"] = redirect_uri

        return backend_class(user_settings, self, **kwargs)
