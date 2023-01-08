from django.http import JsonResponse
from django.shortcuts import render
from .models import Sheep
from tools import login_check
# Create your views here.


@login_check.login_check('GET')
def get_sheeps(request, username):
	if request.method == 'GET':
		token = request.META.get('HTTP_AUTHORIZATION')
		print(token)
		sheeps = Sheep.objects.all()
		list_sheep = []
		for sheep in sheeps:
			dict_sheep = {
				'id': sheep.id,
				'weight': sheep.weight,
				'deal_to': ''
			}
			list_sheep.append(dict_sheep)

		result = {
			'code': 200,
			'data': {
				'sheeps': list_sheep
			}

		}
		return JsonResponse(result)