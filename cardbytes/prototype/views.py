from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from prototype.models import Merchant, User

def index(request):
    return HttpResponse("Hello, Welocome to Cardbytes Prototype.")

def create_merchant(request):
    name = request.GET['name']
    try:
        merchant = Merchant(name=name)
        merchant.save()
        response = {'success': True}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return JsonResponse(response)

def delete_merchant(request):
    id = request.GET['id']
    try:
        merchant = Merchant(id=id).delete()
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

def user(request):
    id = request.GET['id']
    try:
        user = User.objects.filter(id=id).values('id', 'name', \
                'acc_balance', 'cashback_realized')[0]
        data = user.update({'message': 'NA'})
        response = {'success': True, 'user': user}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return JsonResponse(response)


def create_user(request):
    params = request.GET
    name  = params['name']
    acc_balance = 100000
    cashback_realized = 0
    try:
        user = User(name=name, acc_balance=acc_balance, cashback_realized=cashback_realized)
        user.save()
        response = {'success': True}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return JsonResponse(response)
