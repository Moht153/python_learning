from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'/(?P<username>\w*?)/all', views.get_sheeps),
	url(r'/(?P<username>\w*?)/query', views.query_sheeps),
	url(r'/(?P<username>\w*?)/consumer', views.post_consumer),
]