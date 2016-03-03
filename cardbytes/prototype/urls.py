from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^generate_offers$', views.generate_offers, name='generate_offers'),
    url(r'^get_bank_revenue$', views.get_bank_revenue, name='get_bank_revenue'),
    url(r'^get_vendor_revenue$', views.get_vendor_revenue, name='get_vendor_revenue'),
    url(r'^get_merchants$', views.get_merchants, name='get_merchants'),
    url(r'^user$', views.user, name='user'),
    url(r'^transact$', views.transact, name='transact'),
    url(r'^initialize$', views.initialize, name='initialize'),
]
