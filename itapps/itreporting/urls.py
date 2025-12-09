from django.urls import path
from .import views
from .views import PostDetailView, PostListView, PostCreateView
from django.conf import settings
from django.conf.urls.static import static 
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView


app_name = 'itreporting'

urlpatterns = [

    path('',views.home, name= 'home'),
    path('aboutus',views.aboutus, name= 'aboutus'),
    path('contactus',views.contactus, name= 'contactus'),    
    path('report/', PostListView.as_view(), name = 'report'),
    path('issues/<int:pk>', PostDetailView.as_view(), name = 'issue-detail'),
    path('issue/new/', PostCreateView.as_view(), name = 'issue-create'),
    path('issues/<int:pk>/update/', PostUpdateView.as_view(), name = 'issue-update'),
    path('issue/<int:pk>/delete/', PostDeleteView.as_view(), name = 'issue-delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)