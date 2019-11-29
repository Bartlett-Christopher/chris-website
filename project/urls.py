"""Project URL Configuration."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('home.urls', 'home'), namespace='home')),
    path('blog', include(('blog.urls', 'blog'), namespace='blog')),
]
