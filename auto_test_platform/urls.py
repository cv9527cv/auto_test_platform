"""auto_test_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^list_p/$', views.list_projects, name='list_p'),
    re_path('^$', views.list_projects),
    re_path('^add_p/$', views.add_projects, name='add_p'),
    re_path('^edit_p/(?P<id>\d+)$', views.edit_projects, name='edit_p'),
    re_path('^del_p/(?P<id>\d+)$', views.del_projects, name='del_p'),
    re_path('^add_api/(?P<id>\d+)$', views.add_api, name='add_api'),
    re_path('^list_api/(?P<id>\d+)$', views.list_api, name='list_api'),
    re_path('^del_api/(?P<id>\d+)$', views.del_api, name='del_api'),
    re_path('^edit_api/(?P<id>\d+)$', views.edit_api, name='edit_api'),
    re_path('^run_api/(?P<id>\d+)$', views.run_api, name='run_api'),
    re_path('^details_api/(?P<id>\d+)$', views.details_api, name='details_api'),
]
