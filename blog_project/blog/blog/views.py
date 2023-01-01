from django.http import HttpResponse, JsonResponse


def test_api(request):

	return JsonResponse({'code': 200})


