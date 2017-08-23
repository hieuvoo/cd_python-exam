from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^newQuote$', views.newQuote, name="newQuote"),
    url(r'^addFavorite$', views.addFavorite, name="addFavorite"),
    url(r'^removeFavorite$', views.removeFavorite, name="removeFavorite"),
    url(r'^showUser/(?P<userid>\d+)$', views.showUser, name="showUser"),
]
