from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import modelform_factory
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import SSOConfigForm
from .models import AzureADSSOConfig, GitHubSSOConfig, UserDefinedSSOConfig

# The config types that can be created, keyed by the type used in the create url
CONFIG_TYPES = {model.config_type: model for model in (AzureADSSOConfig, GitHubSSOConfig)}


class SSOConfigMixin(PermissionRequiredMixin):

    permission_codename = 'change'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        # Set before dispatch, as the permission check needs it
        self.model = self.get_config_model()

    def get_config_model(self):
        """The existing config's own type"""
        self.object = get_object_or_404(UserDefinedSSOConfig, pk=self.kwargs['pk']).get_subclass_instance()

        return type(self.object)

    def get_object(self, queryset=None):
        return self.object

    def get_permission_required(self):
        meta = self.model._meta
        permission = f'{self.permission_codename}_{meta.model_name}'

        return (f'{meta.app_label}.{permission}',)

    def get_list_url(self) -> str:
        return reverse(f'{self.request.resolver_match.namespace}:list')

    def get_success_url(self):
        return self.get_list_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['config_name'] = self.model._meta.verbose_name
        context['list_url'] = self.get_list_url()

        return context


class SSOConfigFormMixin(SSOConfigMixin):
    template_name = 'social_django_user_config_sso/config_form.html'

    def get_form_class(self):
        return modelform_factory(self.model, form=SSOConfigForm)


class GenericSSOConfigListView(PermissionRequiredMixin, ListView):
    """Every config, whatever its type"""
    model = UserDefinedSSOConfig
    permission_required = 'social_django_user_config_sso.view_userdefinedssoconfig'
    template_name = 'social_django_user_config_sso/config_list.html'
    extra_context = {'config_types': CONFIG_TYPES}


class SSOConfigCreateView(SSOConfigFormMixin, CreateView):
    permission_codename = 'add'

    def get_config_model(self):
        try:
            return CONFIG_TYPES[self.kwargs['config_type']]
        except KeyError:
            raise Http404('Unknown SSO config type')


class SSOConfigUpdateView(SSOConfigFormMixin, UpdateView):
    pass


class SSOConfigDeleteView(SSOConfigMixin, DeleteView):
    permission_codename = 'delete'
    template_name = 'social_django_user_config_sso/config_confirm_delete.html'
