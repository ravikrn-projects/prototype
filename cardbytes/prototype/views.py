from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from prototype.models import Merchant

def index(request):
    return HttpResponse("Hello, Welocome to Cardbytes Prototype.")

def create_merchant(request):
    name = request.GET['name']
    try:
        merchant = Merchant(name = name)
        merchant.save()
        response = {'success': True}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return JsonResponse(response)

def delete_merchant(request):
    id = request.GET['id']
    try:
        merchant = Merchant(id = id).delete()
        response = {'success': True}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return JsonResponse(response)

def get_merchants(request):
    try:
        merchants = Merchant.objects.all().values('id', 'name')
        response = {'success': True, 'merchants': list(merchants)}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return JsonResponse(response)
