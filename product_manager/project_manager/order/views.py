from django.shortcuts import render
from sheeps.models import Sheep
from django.http import JsonResponse
import json
from tools import login_check
# Create your views here.


@login_check.login_check('GET')
def order_info(request, username):
	if request.method == 'GET':
		cust_name = request.GET.get('cust_name')
		if not cust_name:
			cust_name = 'xxx'
		#数据库匹配order
		sheep_list = Sheep.objects.filter(customer__exact=cust_name)
		if sheep_list:
			result_list = []
			for sheep in sheep_list:
				dict_sheep = {
					'id': sheep.id,
					'weight': sheep.weight,
					'deal_to': sheep.customer,
					'single_price': sheep.single_price,
					'total_price': '%.2f' % sheep.total_price,
				}
				if sheep.deal_date:
					dict_sheep['deal_time'] = sheep.deal_date.strftime('%Y-%m-%d')
				else:
					dict_sheep['deal_time'] = None
				result_list.append(dict_sheep)
			result = {
				'code': 200,
				'data': result_list
			}
			return JsonResponse(result)
		else:
			result = {
				'code': 402,
				'err': 'no mathch consumer',
			}
			return JsonResponse(result)

	else:
		result = {
			'code': 401,
			'err': 'please use GET',
		}
		return JsonResponse(result)