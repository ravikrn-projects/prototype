from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^generate_offers$', views.generate_offers, name='generate_offers')
]
