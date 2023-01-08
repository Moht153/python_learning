from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'/(?P<username>\w*?)/all', views.get_sheeps)
]