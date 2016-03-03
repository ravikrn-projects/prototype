from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from prototype.models import Offers, Merchant, Vendor, Bank, User
from config import vendor_commision, bank_commision

def index(request):
    return HttpResponse("Hello, Welocome to Cardbytes Prototype.")

def generate_offers(request):
    params = request.GET
    try:
        offers = Offers.objects.all().values('user_id', 'merchant_id', 'cashback', 'cashback_status')
        offer_list = list(offers)
        offer_list_response = []
        for offer in offer_list:
            offer['merchant'] = Merchant.objects.get(id = offer['merchant_id']).name
            offer_list_response.append(offer)
        response = {'success': True, 'offers': offer_list_response}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return JsonResponse(response)

def get_vendor_revenue(request):
    try:
        vendor = Vendor.objects.all()[0]
        response = {'success': True, 'revenue': vendor.revenue}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return JsonResponse(response)

def get_bank_revenue(request):
    try:
        bank = Bank.objects.all()[0]
        response = {'success': True, 'revenue_without_clm': bank.revenue_without_clm, 
        'revenue_with_clm': bank.revenue_with_clm}
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
    user_id = request.GET['user_id']
    try:
        user = User.objects.filter(id=user_id).values('id', 'name', \
                'acc_balance', 'cashback_realized')[0]
        data = user.update({'message': get_message(user_id)})
        response = {'success': True, 'user': user}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return JsonResponse(response)

def get_message(user_id):
    return 'NA'

def transact(request):
    params = request.GET
    user_id = params['user_id']
    merchant_id = params['merchant_id']
    amount = params['amount']
    try:
        update_user(user_id, merchant_id, amount)
        update_vendor(user_id, merchant_id, amount)
        update_bank(user_id, merchant_id, amount)
        update_status(user_id, merchant_id)
        response = {'success': True}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return JsonResponse(response)

def update_user(user_id, merchant_id, amount):
    user = User.objects.get(id=user_id)
    cashback = get_cashback(user_id, merchant_id, amount)
    user.acc_balance = user.acc_balance - float(amount) + cashback
    user.cashback_realized = cashback
    user.save()

def update_status(user_id, merchant_id):
    if get_cashback(user_id, merchant_id)>0
        offer = Offers.objects.filter(user_id=user_id, merchant_id=merchant_id)
        offer.cashback_status = 'used'
    else:
        return 

def update_vendor(user_id, merchant_id, amount):
    cashback = get_cashback(user_id, merchant_id)
    vendor_commision_amt = vendor_commision*cashback
    vendor = Vendor.objects.all()[0]
    vendor.revenue +=vendor_commision_amt
    vendor.save()

def update_bank(user_id, merchant_id, amount):
    cashback = get_cashback(user_id, merchant_id)
    clm_commision = bank_clm_commision*vendor_commision*cashback
    transaction_commision = bank_commision*amount
    bank = Bank.objects.all()[0]
    bank.revenue_with_clm += transaction_commision+clm_commision
    bank.revenue_without_clm += transaction_commision
    bank.save()

def get_cashback(user_id, merchant_id):
    cashback = 0
    try:
        offer = Offers.objects.filter(user_id=user_id, merchant_id=merchant_id)
        if len(offer)>0:
            cashback = offer.cashback
    except Exception as e:
        pass
    return cashback

def initialize(request):
    try:
        #delete previous data
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