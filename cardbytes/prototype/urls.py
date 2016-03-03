from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^generate_offers$', views.generate_offers, name='generate_offers'),
    url(r'^create_merchant$', views.create_merchant, name='create_merchant'),
    url(r'^delete_merchant$', views.delete_merchant, name='delete_merchant'),
    url(r'^get_merchants$', views.get_merchants, name='get_merchants'),
    url(r'^get_bank_revenue$', views.get_bank_revenue, name='get_bank_revenue'),
    url(r'^get_vendor_revenue$', views.get_vendor_revenue, name='get_vendor_revenue'),
]
