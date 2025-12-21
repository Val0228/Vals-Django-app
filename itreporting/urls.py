from django.urls import path
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    ModuleListView, ModuleDetailView
)

app_name = 'itreporting'

urlpatterns = [
    path('', views.home, name='home'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('contactus/', views.contactus, name='contactus'),    
    path('report/', PostListView.as_view(), name='report'),
    path('issues/<int:pk>/', PostDetailView.as_view(), name='issue-detail'),
    path('issue/new/', PostCreateView.as_view(), name='issue-create'),
    path('issues/<int:pk>/update/', PostUpdateView.as_view(), name='issue-update'),
    path('issue/<int:pk>/delete/', PostDeleteView.as_view(), name='issue-delete'),
    # Module URLs
    path('modules/', ModuleListView.as_view(), name='module-list'),
    path('modules/<int:pk>/', ModuleDetailView.as_view(), name='module-detail'),
    path('modules/<int:pk>/enroll/', views.enroll_module, name='module-enroll'),
    path('modules/<int:pk>/cancel/', views.cancel_enrollment, name='module-cancel'),
    path('modules/<int:pk>/submit/', views.submit_module, name='module-submit'),
    # Weather URLs
    path('weather/', views.weather, name='weather'),
    path('api/weather/', views.weather_api, name='weather-api'),
    # News API URL
    path('api/news/', views.news_api, name='news-api'),
]