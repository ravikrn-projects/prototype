from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from prototype.models import Merchant, User, Offers

def index(request):
    return HttpResponse("Hello, Welocome to Cardbytes Prototype.")

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

def transact(request):
    params = request.GET
    user_id = params['user_id']
    merchant_id = params['merchant_id']
    amount = params['amount']
    try:
        update_user(user_id, merchant_id, amount)
        update_vendor(user_id, merchant_id, amount)
        update_bank(user_id, merchant_id, amount)
        response = {'success': True}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return JsonResponse(response)

def update_user(user_id, merchant_id, amount):
    user = User.objects.get(id=user_id)
    user.acc_balance -= float(amount)
    user.cashback_realized = get_cashback(user_id, merchant_id, amount)
    user.save()

def get_cashback(user_id, merchant_id, amount):
    return 0

def update_vendor(user_id, merchant_id, amount):
    pass

def update_bank(user_id, merchant_id, amount):
    pass

def initialize(request):
    try:
        # delete previous data
        User.objects.all().delete()
        Merchant.objects.all().delete()
        Offers.objects.all().delete()

        #insert new data
        user_names = ['Ravi', 'Akash']
        acc_balance = 10000
        for user_name in user_names:
            user = User(name=user_name, acc_balance=acc_balance, cashback_realized=0)
            user.save()

        merchant_names = ['McDonalds', 'KFC', 'PizzaHut', 'Dominos']
        for merchant_name in merchant_names:
            merchant = Merchant(name=merchant_name)
            merchant.save()

        response = {'success': True}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return JsonResponse(response)
