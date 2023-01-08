from django.conf.urls import url
from . import views

urlpatterns = [
	# http://127.0.0.1:8000/v1/users
	url(r'^$', views.users),
	#http://127.0.0.1:8000/v1/users/<username>
	#APPENT_SLASH 自动补全url后面的斜杠，前提是你有一个带/ 结尾的路由
]