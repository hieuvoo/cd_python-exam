"""quotablequotes URL Configuration
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^quotes/', include('apps.quotes.urls', namespace="quotes")),
    url(r'^', include('apps.login.urls', namespace="auth")),
]
