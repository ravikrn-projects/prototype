from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_merchant$', views.create_merchant, name='create_merchant'),
    url(r'^delete_merchant$', views.delete_merchant, name='delete_merchant'),
    url(r'^get_merchants$', views.get_merchants, name='get_merchants'),
    url(r'^user$', views.user, name='user'),
    url(r'^create_user$', views.create_user, name='create_user'),
    url(r'^transact$', views.transact, name='transact'),
    url(r'^initialize$', views.initialize, name='initialize'),
]
