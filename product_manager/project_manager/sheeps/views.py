import json

from django.http import JsonResponse
from django.shortcuts import render
from .models import Sheep
from tools import login_check
# Create your views here.


@login_check.login_check('GET')
def get_sheeps(request, username):
	if request.method == 'GET':
		start = request.GET.get('start')
		end = request.GET.get('end')
		print(start, end)

		result = get_sheep(start, end)
		return JsonResponse(result)
		# sheeps = Sheep.objects.all()
		# list_sheep = []
		# for sheep in sheeps:
		# 	dict_sheep = {
		# 		'id': sheep.id,
		# 		'weight': sheep.weight,
		# 		'deal_to': sheep.customer,
		# 		'single_price': sheep.single_price,
		# 		'total_price': sheep.total_price,
		# 	}
		# 	if sheep.deal_date:
		# 		dict_sheep['deal_time'] = sheep.deal_date.strftime('%Y-%m-%d %H:%M:%S')
		# 	else:
		# 		dict_sheep['deal_time'] = None
		# 	list_sheep.append(dict_sheep)
		#
		#
		# result = {
		# 	'code': 200,
		# 	'data': {
		# 		'sheeps': list_sheep
		# 	}
		#
		# }
		# return JsonResponse(result)


def get_sheep(start, end):
	sheeps = Sheep.objects.filter(id__gt=int(start) - 1, id__lt=end)
	if not sheeps:
		result = {
			'code': 205,
			'error': '到头啦！'
		}
		return result
	list_sheep = []
	for sheep in sheeps:
		if sheep.memo == '净重计算':
			dict_sheep = {
				'id': sheep.id,
				'weight': sheep.real_weight,
				'deal_to': sheep.customer,
				'single_price': sheep.single_price,
				'total_price': '{:.2f}'.format(float(sheep.total_price)),
			}
		else:
			dict_sheep = {
				'id': sheep.id,
				'weight': sheep.weight,
				'deal_to': sheep.customer,
				'single_price': sheep.single_price,
			}
		if sheep.total_price:
			dict_sheep['total_price'] = '{:.2f}'.format(float(sheep.total_price)),
		else:
			dict_sheep['total_price'] = None
		if sheep.deal_date:
			dict_sheep['deal_time'] = sheep.deal_date.strftime('%Y-%m-%d')
		else:
			dict_sheep['deal_time'] = None
		list_sheep.append(dict_sheep)
	result = {
		'code': 200,
		'data': {
			'sheeps': list_sheep,
			'end': end
		}
	}
	return result


@login_check.login_check('GET')
def query_sheeps(request, username):
	if request.method == 'GET':
		id = request.GET.get('id')
		if not id:
			result = {
				'code': 201,
				'error': 'please give me id'
			}
			return JsonResponse(result)
		try:
			sheep = Sheep.objects.get(id=id)
		except Exception as e:
			print(e)
			result = {
				'code': 202,
				'error': 'wrong id'
			}
			return JsonResponse(result)

		print("query:", sheep.id, sheep.weight)

		real_weight = sheep.real_weight
		if not sheep.real_weight:
			real_weight = 0

		result = {
			'code': 200,
			'data': {
				'id': sheep.id,
				'weight': sheep.weight,
				'real_weight': real_weight
			}
		}
		return JsonResponse(result)


@login_check.login_check('POST')
def post_consumer(request, username):
	if request.method == 'POST':
		json_str = request.body
		# json字符串转对象
		json_obj = json.loads(json_str)
		print(json_str)
		if not json_obj:
			result = {
				'code': 301,
				'error': 'no json'
			}
			return JsonResponse(result)
		# 以下是常规检查：
		cust_name = json_obj.get('consumer')
		if not cust_name:
			result = {
				'code': 302,
				'error': 'no consumer'
			}
			return JsonResponse(result)

		total_price = json_obj.get('total_price')
		if not total_price:
			result = {
				'code': 303,
				'error': 'no total_price'
			}
			return JsonResponse(result)

		is_real_weight = json_obj.get('is_real')
		if not is_real_weight:
			result = {
				'code': 304,
				'error': 'no is_real param'
			}
			return JsonResponse(result)

		sheep_id = json_obj.get('id')
		if not sheep_id:
			result = {
				'code': 305,
				'error': 'need id'
			}
			return JsonResponse(result)

		sheep_single_price = json_obj.get('single_price')
		if not sheep_single_price:
			result = {
				'code': 306,
				'error': 'no single_price'
			}
			return JsonResponse(result)
		sheep_real_weight = json_obj.get('real_weight')
		# 根据sheep_id 匹配商品
		try:
			sheep = Sheep.objects.get(id=sheep_id)
		except:
			result = {
				'code': 307,
				'error': 'no match sheep'
			}
			return JsonResponse(result)

		# # 开始修改参数
		sheep.single_price = sheep_single_price
		if is_real_weight == '1':
			sheep.memo = '毛重计算'
		elif is_real_weight == '0':
			sheep.memo = '净重计算'
		sheep.real_weight = sheep_real_weight
		sheep.total_price = total_price
		sheep.customer = cust_name
		sheep.save()

		result = {
			'code': 200,
			'msg': '订单存储完毕'
		}
		return JsonResponse(result)