from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^request/(?P<id>[\d]+)/$', views.request, name='request'),
	url(r'^tariff_order/(?P<id>[\d]+)/$', views.tariff_order, name='tariff_order'),
]
