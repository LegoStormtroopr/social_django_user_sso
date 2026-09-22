from django.forms import modelform_factory
from django.urls import include, path

from . import models, views
from .forms import SSOConfigForm

app_name = 'sso_config'


def config_urls(model, form_class=None):
    """The four config pages for one UserDefinedSSOConfig subclass"""
    if form_class is None:
        form_class = modelform_factory(model, form=SSOConfigForm)

    view_kwargs = {'model': model}
    form_kwargs = dict(view_kwargs, form_class=form_class)

    return [
        path('', views.SSOConfigListView.as_view(**view_kwargs), name='list'),
        path('new/', views.SSOConfigCreateView.as_view(**form_kwargs), name='create'),
        path('<int:pk>/', views.SSOConfigUpdateView.as_view(**form_kwargs), name='update'),
        path('<int:pk>/delete/', views.SSOConfigDeleteView.as_view(**view_kwargs), name='delete'),
    ]


urlpatterns = [
    path('azure/', include((config_urls(models.AzureADSSOConfig), 'azure'))),
    path('github/', include((config_urls(models.GitHubSSOConfig), 'github'))),
]
