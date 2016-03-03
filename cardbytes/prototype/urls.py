from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_merchants$', views.get_merchants, name='get_merchants'),
    url(r'^user$', views.user, name='user'),
    url(r'^transact$', views.transact, name='transact'),
    url(r'^initialize$', views.initialize, name='initialize'),
]
