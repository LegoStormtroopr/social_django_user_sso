from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("", views.LoginTemplateView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name='logout'),
    path('', include('social_django.urls', namespace='social')),
    path('sso/', include('social_django_user_config_sso.urls', namespace='sso_config')),
    path("admin/", admin.site.urls),
]
