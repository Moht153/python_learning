from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'/(?P<username>\w*?)/info', views.order_info),
]