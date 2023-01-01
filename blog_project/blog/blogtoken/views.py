import hashlib
import json
import time

import jwt

from user.models import UserProfile
from django.http import JsonResponse

# Create your views here.


def tokens(request):
	"""
	创建token == 登陆
	：param request:
	:return 
	"""
	if not request.method == 'POST':
		return JsonResponse({'code': 100, 'error': 'Please use POST'})

	# 获取前端传来的数据/生成token
	user_str = request.body
	if not user_str:
		result = {'code': 102, 'error': 'Please give me json'}
		return JsonResponse(result)

	json_obj = json.loads(user_str)
	username = json_obj.get('username')
	password = json_obj.get('password')
	if not username:
		result = {'code': 103, 'error': 'Please give me username'}
		return JsonResponse(result)
	if not password:
		result = {'code': 104, 'error': 'Please give me password'}
		return JsonResponse(result)


	###### 校验数据 ########
	users = UserProfile.objects.filter(username__exact=username)
	# print(users)
	# print(type(users))
	if not users:
		result = {'code': 105, 'error': 'Your username or password is wrong!'}
		return JsonResponse(result)


	# 获取-校验密码-生成token
	# 比较密码
	user = users[0]
	m = hashlib.md5()
	m.update(password.encode())
	password = m.hexdigest()
	if user.password == password:
		# make token
		token = make_token(username)
		# 正常返回给前端
		result = {'code': 200, 'username': username, 'data': {'token': token}}
		return JsonResponse(result)
	else:
		result = {'code': 106, 'error': 'Your username or password is wrong!'}
		return JsonResponse(result)


def make_token(user_name, expire=24*3600):

	# 官方jwt / 自定义jwt

	payload = {'username': user_name, 'exp': time.time() + expire}
	key = '123456'
	token = jwt.encode(payload, key, algorithm='HS256')
	return token


def decode_token(token):
	key = '123456'
	payload = jwt.decode(token, key, algorithms='HS256')
	return payload
