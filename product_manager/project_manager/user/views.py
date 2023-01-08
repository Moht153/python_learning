import json
import hashlib
from django.http import JsonResponse
from .models import UserProfile
from django.db import utils
from user_token.views import make_token, decode_token
from tools.login_check import *
# Create your views here.


@login_check('PUT', 'GET')
def users(request, username=None):

	if request.method == 'GET':
		# 获取用户数据
		if username:
			# /v1/users/<username>
			# 拿指定用户数据
			try:
				user = UserProfile.objects.get(username=username)
			except Exception as e:
				user = None
			if not user:
				result = {'code': 208, 'error': 'No user'}
				return JsonResponse(result)
			# 检查是否有查询字符串 例如：/v1/users/<username>?aa=xxxx&b=XXXX...
			if request.GET.keys():
				# 查询指点字段
				data = {}
				# 遍历查询字段
				for k in request.GET.keys():
					# 检查是否存在查询字段属性
					if hasattr(user, k):
						# 如果有：提取字段属性
						v = getattr(user, k)
						if k == 'avatar':
							data[k] = str(v)
						else:
							data[k] = v
				# 生成json对象
				result = {'code': 200, 'username': username, 'data': data}
				return JsonResponse(result)
			else:
				# 全量查询[password，email 不给]
				result = {'code': 200, 'username': username, 'data': {
					 'avatar': str(user.avatar), 'nickname': user.nickname
				}}
				return JsonResponse(result)
		else:
			# /v1/users
			return JsonResponse({'code': 200, 'error': 'wolaila'})

	elif request.method == 'POST':
		# 此功能模块异常码 201 开始
		# 创建用户
		# 前端注册页面地址 http://127.0.0.1:5000/register
		# print(request.POST.get('username', '??'))  # 结果发现无法获取username
		# 结论 request.POST.get() 方法只可以拿表单POST提交的数据
		# print(request.body)
		# dict_ = json.load(request.body)

		#读取用户注册信息
		json_str = request.body
		print(json_str)
		# 处理没有数据
		if not json_str:
			result = {'code': 201, 'error': 'Please give me data'}
			return JsonResponse(result)

		json_obj = json.loads(json_str)

		# 处理没有用户名
		user_name = json_obj.get('username')
		if not user_name:
			result = {'code': 202, 'error': 'Please give me username'}
			return JsonResponse(result)

		email = json_obj.get('email')
		if not email:
			result = {'code': 203, 'error': 'Please give me email'}
			return JsonResponse(result)

		passwd1 = json_obj.get('password_1')
		passwd2 = json_obj.get('password_2')
		if not passwd1 or not passwd2:
			result = {'code': 204, 'error': 'Please give me password'}
			return JsonResponse(result)

		# 先做密码比对
		if passwd1 != passwd2:
			return JsonResponse({'code': 205, 'error': 'Your password are not same'})

		# 优先查询当前用户名是否已经存在
		old_user = UserProfile.objects.filter(username=user_name)
		if old_user:
			result = {'code': 206, 'error': 'Your username is already existed'}
			return JsonResponse(result)


		# 给密码做hash md5哈希/散列 加密
		m = hashlib.md5()
		m.update(passwd1.encode())
		passwd1 = m.hexdigest()


		try:
			UserProfile.objects.create(
				username=user_name,
				email=email,
				password=passwd1,
			)

		except utils.IntegrityError as err:
			# print(err)
			# 数据库down了，用户名已存在
			result = {'code': 207, 'msg': err.__str__()}
			return JsonResponse(result)
		else:
			token = make_token(user_name)
			# 正常返回给前端
			result = {'code': 200, 'username': user_name, 'data': {'token': token}}
			return JsonResponse(result)

	elif request.method == 'PUT':
		# http://127.0.0.1:5000/<username>/change_info
		# 更新数据
		# 此头可获取前端传来的token
		# META 可拿去http协议原生头， META 也是类字典对象，可使用字典相关方法
		# 特别注意： http头有可能被django 重命名， 建议百度

		# 先做校验 username是否跟token中的一致


		info_change = request.body

		info_change = json.loads(info_change)
		print(type(info_change))

		# 修改用户信息
		user = request.user
		# 方法一：
		if not info_change['nickname']:
			result = {'code': 212, 'error': 'no nickname'}
			return JsonResponse(result)
		if not info_change['sign']:
			result = {'code': 210, 'error': 'no sign'}
			return JsonResponse(result)
		if not info_change['info']:
			result = {'code': 211, 'error': 'no info'}
			return JsonResponse(result)

		user.sign = info_change.get('sign')
		user.info = info_change.get('info')
		user.nickname = info_change.get('nickname')

		# 方法二：
		# if not info_change['sign'] and not info_change['info'] and not info_change['nickname']:
		# 	result = {'code': 210, 'error': 'Please offer any one of sign, info and nickname'}
		# 	return JsonResponse(result)
		# for k in info_change:
		# 	if info_change[k]:
		# 		setattr(user, k, info_change[k])

		user.save()
		return JsonResponse({'code': 200, 'error': 'update complete'})

	else:
		raise
	return JsonResponse({'code': 200})