from django.urls import path

from . import views

app_name = 'sso_config'

urlpatterns = [
    path('', views.GenericSSOConfigListView.as_view(), name='list'),
    path('<str:config_type>/new/', views.SSOConfigCreateView.as_view(), name='create'),
    path('<int:pk>/', views.SSOConfigUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.SSOConfigDeleteView.as_view(), name='delete'),
]
