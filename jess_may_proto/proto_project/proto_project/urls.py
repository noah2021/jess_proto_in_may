"""proto_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# -*- coding: utf-8 -*-

import os.path
from django.conf.urls import *
from django.contrib import admin
from bookmarks import views
from django.views.generic import TemplateView


site_media = os.path.join(
    os.path.dirname(__file__), 'site_media'
)


urlpatterns = patterns('',
           # 북마크 조회
           (r'^$', views.main_page),
           (r'^user/(\w+)/$', views.user_page),

           # 세션관리
           (r'^login/$', 'django.contrib.auth.views.login'),
           (r'^logout/$', views.logout_page),
           (r'^register/$', views.register_page),
           (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
              { 'document_root' : site_media }),
                       (r'^register/success/$', TemplateView,
                        {'template':'registration/register_success.html' }),

           # 계정관리
           (r'^save/$', views.bookmark_save_page),
           (r'^tag/([^\s]+)/$', views.tag_page),

           (r'^tag/$', views.tag_cloud_page),
                       (r'^search/$', views.search_page),
           )