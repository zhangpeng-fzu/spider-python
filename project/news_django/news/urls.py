"""news URL Configuration

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
from django.urls import path
from project.news import home
from project.news import user_view
from project.news import news_view
from project.news import security_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.index),
    path('login', user_view.login),
    path('users/', user_view.user_list),
    path('users/delete', user_view.delete),
    path('news/list', news_view.news_list),
    path('news/delete', news_view.delete),
    path('news/spider', news_view.spider),
    path('news/label', news_view.label),
    path('news/label/delete', news_view.deleteLabel),
    path('security/whiteip', security_view.whiteip),
    path('security/whiteip/delete', security_view.deleteAll)
]
