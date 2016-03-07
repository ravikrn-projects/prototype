import random
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from prototype.models import Offer, Merchant, Vendor, Bank, User, Relevance
from config import vendor_commission, bank_commission, bank_commission_clm,\
        tags, geography, goals

def index(request):
    context = {'data': 'Hello'}
    return render(request, 'index.html', context)

def customer(request, user_id):
    context = {'user_id': user_id}
    return render(request, 'customer.html', context)


def backend_analytics(request):
    return render(request, 'backend_analytics.html')

def merchant(request, merchant_id):
    context = {'merchant_id': merchant_id,
               'tags': json.dumps(tags),
               'geography': json.dumps(geography),
               'goals': json.dumps(goals)}
    return render(request, 'merchant.html', context)

def show_offers(request):
    params = request.GET
    try:
        offers = Offer.objects.all().values()
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
    res = JsonResponse(response)
    res["Access-Control-Allow-Origin"] = "*"
    return res

def user(request):
    user_id = request.GET['user_id']
    try:
        user = User.objects.filter(id=user_id).values('id', 'name', \
                'acc_balance', 'cashback_realized')[0]
        data = user.update({'message': get_message(user_id)})
        response = {'success': True, 'user': user}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    res = JsonResponse(response)
    res["Access-Control-Allow-Origin"] = "*"
    return res

def get_message(user_id):
    try:
        offer = Offer.objects.get(user_id=user_id)
        merchant = Merchant.objects.get(id=offer.merchant_id)
        message = 'Get ' + str(offer.cashback * 100) + '% cashback on transaction at ' + merchant.name
    except Exception:
        message = ''    
    return message

def transact(request):
    params = request.GET
    user_id = params['user_id']
    merchant_id = params['merchant_id']
    amount = float(params['amount'])
    try:
        cashback = get_cashback(user_id, merchant_id)
        update_user(user_id, cashback, amount)
        update_vendor(cashback, amount)
        update_bank(cashback, amount)
        update_status(user_id, merchant_id, cashback)
        response = {'success': True}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    res = JsonResponse(response)
    res["Access-Control-Allow-Origin"] = "*"
    return res

def update_user(user_id, cashback, amount):
    user = User.objects.get(id=user_id)
    user.acc_balance = user.acc_balance - float(amount) + amount*cashback
    user.cashback_realized = amount * cashback
    user.save()

def update_status(user_id, merchant_id, cashback):
    if cashback>0:
        offer = Offer.objects.get(user_id=user_id, merchant_id=merchant_id)
        offer.cashback_used = True
        offer.save()

def update_vendor(cashback, amount):
    vendor_commission_amt = vendor_commission*cashback
    vendor = Vendor.objects.all()[0]
    vendor.revenue += vendor_commission_amt*amount
    vendor.save()

def update_bank(cashback, amount):
    clm_commission = bank_commission_clm*vendor_commission*cashback*amount
    transaction_commission = bank_commission*amount
    bank = Bank.objects.all()[0]
    bank.revenue_with_clm += transaction_commission+clm_commission
    bank.revenue_without_clm += transaction_commission
    bank.save()

def get_cashback(user_id, merchant_id):
    cashback = 0
    try:
        offer = Offer.objects.get(user_id=user_id, merchant_id=merchant_id)    
        cashback = offer.cashback
    except Exception as e:
        pass
    return cashback

def initialize(request):
    try:
        #delete previous data
        User.objects.all().delete()
        Merchant.objects.all().delete()
        Offer.objects.all().delete()
        Vendor.objects.all().delete()
        Bank.objects.all().delete()
        # insert new data
        initialize_users()
        initialize_merchants()
        initialize_vendor()
        initialize_bank()

        response = {'success': True}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return JsonResponse(response)

def initialize_users():
    user_names = ['A', 'B', 'C', 'D']
    acc_balance = 10000
    for user_name in user_names:
        user = User(name=user_name, acc_balance=acc_balance, cashback_realized=0)
        user.save()

def initialize_merchants():
    merchant_names = ['McDonalds', 'KFC', 'PizzaHut', 'Dominos']
    for merchant_name in merchant_names:
        merchant = Merchant(name=merchant_name)
        merchant.save()
        
def generate_offer(request):
    params = request.GET
    merchant_id = params['merchant_id']
    cashback = float(params['cashback'])/100
    goal_id = params['goal_id']
    customer_tag_id = params['customer_tag_id']
    geography_id = params['geography_id']
    try:
        merchant = Merchant.objects.get(id=merchant_id)
        offer = Offer(merchant=merchant,
                      cashback=cashback,
                      cashback_used=False,
                      goal=goal_id,
                      customer_tag=customer_tag_id,
                      geography=geography_id
                     )
        offer.save()
        response = {'success': True}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    res = JsonResponse(response)
    res["Access-Control-Allow-Origin"] = "*"
    return res

def initialize_vendor():
    vendor = Vendor()
    vendor.save()

def initialize_bank():
    bank = Bank()
    bank.save()


def get_relevance_data(request):
    data = {'unique_id': [], 'index': []}
    try:
        relevance_data = Relevance.objects.all()
        for user in relevance_data:
            data['unique_id'].append(user.unique_id)
            data['index'].append(user.index)
        response = {'success': True, 'data': data}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return JsonResponse(response)