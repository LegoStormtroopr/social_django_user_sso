from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import SSOConfigForm, mask

# Views are parameterised by model rather than being written for each config


class SSOConfigMixin(PermissionRequiredMixin):

    permission_codename = 'change'

    def get_permission_required(self):
        meta = self.model._meta
        permission = f'{self.permission_codename}_{meta.model_name}'

        return (f'{meta.app_label}.{permission}',)

    def config_url(self, name: str, *args) -> str:
        """Reverse one of this model's routes, under the namespace it is included in"""
        namespace = self.request.resolver_match.namespace
        if namespace:
            name = f'{namespace}:{name}'

        return reverse(name, args=args)

    def get_success_url(self):
        return self.config_url('list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['config_name'] = self.model._meta.verbose_name
        context['list_url'] = self.config_url('list')

        return context


class SSOConfigListView(SSOConfigMixin, ListView):
    permission_codename = 'view'
    template_name = 'social_django_user_config_sso/config_list.html'

    def get_columns(self):
        columns = []
        for field in self.model._meta.fields:
            # Skips the id and the pk
            if field.name == 'id' or field.primary_key:
                continue

            columns.append(field.name)

        return columns

    def get_row(self, config, columns):
        values = []
        for name in columns:
            value = getattr(config, name)
            if name in SSOConfigForm.secret_fields:
                value = mask(value)

            values.append(value)

        return {
            'values': values,
            'edit_url': self.config_url('update', config.pk),
            'delete_url': self.config_url('delete', config.pk),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        columns = self.get_columns()

        context['create_url'] = self.config_url('create')
        context['columns'] = columns
        context['rows'] = [self.get_row(config, columns) for config in context['object_list']]

        return context


class SSOConfigCreateView(SSOConfigMixin, CreateView):
    permission_codename = 'add'
    template_name = 'social_django_user_config_sso/config_form.html'


class SSOConfigUpdateView(SSOConfigMixin, UpdateView):
    template_name = 'social_django_user_config_sso/config_form.html'


class SSOConfigDeleteView(SSOConfigMixin, DeleteView):
    permission_codename = 'delete'
    template_name = 'social_django_user_config_sso/config_confirm_delete.html'
