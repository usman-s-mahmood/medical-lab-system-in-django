"""
URL configuration for LabSystemProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf import urls as conf_urls
from BlogApp.views import not_found, server_error
import BlogApp

urlpatterns = [
    path('admin-area/', admin.site.urls),
    path('', include('BlogApp.urls'), name='blog-app-urls'),
    path('lab/', include('LabApp.urls'), name='lab-app-urls'),
    path('auth/', include('AuthApp.urls'), name='auth-app-urls'),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

admin.site.site_header = 'Lab Management Project'
admin.site.site_title = 'Administrative Panel'
admin.site.index_title = 'Programming for Big Data project | Demonstration of Medical Laboratory Automation'

conf_urls.handler400  = BlogApp.views.not_found
conf_urls.handler500 = server_error