# social_django_user_sso


# AUTHENTICATION_BACKENDS

Every allowed UserDefined backend must be listed in AUTHENTICATION_BACKENDS

# Setting Up

There must be a UserDefined Subclass in .backends for anything we want to authenticate with.
This must have a corresponding Django model in .models

# Setting Up Models

* Each User config model must be subclassed from UserDefinedSSOConfig
* It must have a 'psa_backend_name' that corresponse with the name of the backend in [python-social-auth](https://python-social-auth.readthedocs.io/)
* It must provide a 'get_social_auth_settings' that provides the authentication information for that specific authentication method


TODO:
* Add oidc support

# Changelog
* Switched to tenant specific backend for azure, fixed escaped help text

# Starting stuff up

>  uv run ./dev/project/manage.py runserver 0.0.0.0:8000