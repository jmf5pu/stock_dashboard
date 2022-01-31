"""stock_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.views.generic.base import TemplateView
from stock import views as stock_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', stock_views.pie_chart, name='home'),
    #path('', include('stock.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^signup/$', stock_views.signup, name='signup'),
    url(r'^add_asset/$', stock_views.add_asset, name='add_asset'),
    url(r'^remove_asset/$', stock_views.remove_asset, name='remove_asset'),
    url(r'^not_found/$', stock_views.not_found, name='not_found'),
    url(r'^info/$', stock_views.info, name='info'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
