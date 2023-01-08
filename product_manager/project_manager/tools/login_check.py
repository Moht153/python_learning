import jwt
from django.http import JsonResponse
from user.models import UserProfile

KEY = '123456'


# 传参装饰器
# login_check('PUT','GET','POST')
def login_check(*method):
	def _login_check(func):

		def wrapper(request, *args, username=None, **kwargs):
			# 通过request检查token
			# 校验不通过，return JsonResponse()
			# user 查询出来
			token = request.META.get('HTTP_AUTHORIZATION')

			# 这一步很重要，是实现传参装饰器的关键
			if request.method not in method:
				# 返回users视图函数，里面有对应的处理方法（raise）
				return func(request, username, *args, **kwargs)
			if not token:
				result = {'code': 107, 'error': 'Please login'}
				return JsonResponse(result)
			try:
				res = jwt.decode(token, KEY, algorithms=['HS256'])
			except jwt.ExpiredSignatureError:
				# token过期了
				result = {'code': 108, 'error': 'Please login'}
				return JsonResponse(result)
			except Exception as e:
				result = {'code': 109, 'error': 'Please login'}
				return JsonResponse(result)

			# 完整版，比较解析出来的username和url传过来的username是否一致
			if res['username'] != username:
				result = {'code': 111, 'error': "username in url is different with the one in token"}
				return JsonResponse(result)


			# request插入一条键值对

			try:
				user = UserProfile.objects.get(username=res['username'])
			except:
				user = None
			if not user:
				result = {'code': 110, 'error': 'no user'}
				return JsonResponse(result)
			# 将查询成功的user对象赋值给request
			request.user = user
			return func(request, username, *args, **kwargs)

		return wrapper
	return _login_check


def get_user_by_request(request):
	"""
	通过request, 尝试获取user
	@param request:
	@return: UserProfile obj   or  None
	"""
	token = request.META.get('HTTP_AUTHORIZATION')
	if not token:
		return None
	try:
		res = jwt.decode(token, KEY, algorithms=['HS256'])
	except:
		return None
	username = res['username']
	try:
		user = UserProfile.objects.get(username=username)
	except:
		return None

	return user


# 传参装饰器2
# login_check('PUT','GET','POST')
def login_check2(*method):
	def _login_check(func):

		def wrapper(request,  *args, **kwargs):
			# 通过request检查token
			# 校验不通过，return JsonResponse()
			# user 查询出来
			token = request.META.get('HTTP_AUTHORIZATION')

			# 这一步很重要，是实现传参装饰器的关键
			if request.method not in method:
				# 返回users视图函数，里面有对应的处理方法（raise）
				return func(request, *args, **kwargs)
			if not token:
				result = {'code': 107, 'error': 'Please login'}
				return JsonResponse(result)
			try:
				res = jwt.decode(token, KEY, algorithms=['HS256'])
			except jwt.ExpiredSignatureError:
				# token过期了
				result = {'code': 108, 'error': 'Please login'}
				return JsonResponse(result)
			except Exception as e:
				result = {'code': 109, 'error': 'Please login'}
				return JsonResponse(result)

			# request插入一条键值对

			try:
				user = UserProfile.objects.get(username=res['username'])
			except:
				user = None
			if not user:
				result = {'code': 110, 'error': 'no user'}
				return JsonResponse(result)
			# 将查询成功的user对象赋值给request
			request.user = user
			return func(request, *args, **kwargs)

		return wrapper
	return _login_check
