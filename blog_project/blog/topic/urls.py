from django.conf.urls import url
from . import views


urlpatterns = [
	# http://127.0.0.1/v1/topics/<username>
	url(r'^/(?P<username>[\w]{1,11})$', views.topics),
]