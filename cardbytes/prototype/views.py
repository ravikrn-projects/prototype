import csv
import os
import json
import datetime
import time

from collections import defaultdict
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from prototype.models import Offer, Merchant, Vendor, Bank, User, Relevance, Transaction
from config import vendor_commission, bank_commission, bank_commission_clm,\
        income_tag, customer_tag, goals, urls

def index(request):
    context = {
               'get_vendor_revenue_url': urls['get_vendor_revenue'],
               'get_bank_revenue_url': urls['get_bank_revenue'],
               'show_offers_url': urls['show_offers']
               }
    return render(request, 'index.html', context)

def customer(request, user_id):
    context = {'user_id': user_id,
               'transact_url': urls['transact'],
               'user_url': urls['user'],
               'get_merchants_url': urls['get_merchants']
            }
    return render(request, 'customer.html', context)

def backend_analytics(request):
    context = {'get_relevance_data_url': urls['get_relevance_data']
            }
    return render(request, 'backend_analytics.html', context)

def merchant(request, merchant_id):
    context = {'merchant_id': merchant_id,
               # 'income_tag': json.dumps(income_tag),
               # 'customer_tag': json.dumps(customer_tag),
               'goals': json.dumps(goals),
               'get_transaction_data_url': urls['get_transaction_data'],
               'generate_offer_url': urls['generate_offer']
               }
    return render(request, 'merchant.html', context)

def show_offers(request):
    params = request.GET
    try:
        offers = Offer.objects.all().values()
        offer_list = list(offers)
        offer_list_response = []
        for offer in offer_list:
            offer['merchant'] = Merchant.objects.get(merchant_id = offer['merchant_id']).name
            offer['goal'] = goals[offer['goal']]['name'] 
            # offer['income_tag'] = income_tag[offer['income_tag']]['name'] 
            # offer['customer_tag'] = customer_tag[offer['customer_tag']]['name'] 
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
        merchants = Merchant.objects.all().values()
        response = {'success': True, 'merchants': list(merchants)}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    res = JsonResponse(response)
    res["Access-Control-Allow-Origin"] = "*"
    return res

def user(request):
    user_id = request.GET['user_id']
    try:
        user = User.objects.filter(user_id=user_id).values()[0]
        data = user.update({'message': get_message(user_id)})
        response = {'success': True, 'user': user}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    res = JsonResponse(response)
    res["Access-Control-Allow-Origin"] = "*"
    return res

def get_message(user_id):
    try:
        user = User.objects.get(user_id=user_id)
        # income_tag = user.income_tag
        # customer_tag = user.customer_tag
        # all_offer = Offer.objects.all()   
        # offer = all_offer[len(all_offer)-1]
        # merchant = Merchant.objects.get(merchant_id=offer.merchant_id)
        # message = 'Get ' + str(offer.cashback * 100) + '% cashback on transaction at ' + merchant.name
        message = user.message
    except Exception:
        message = ''    
    return message

def transact(request):
    params = request.GET
    try:
        try:
            transaction_id = Transaction.objects.latest('transaction_id').transaction_id + 1
        except Exception:
            transaction_id = 0
        data = {
            'transaction_id': transaction_id,
            'user_id': params['user_id'],
            'merchant_id': params['merchant_id'],
            'amount': params['amount'],
            'timestamp': time.time(),
            'bank_id': 0
        }    
        transact_update(data)
        response = {'success': True}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    res = JsonResponse(response)
    res["Access-Control-Allow-Origin"] = "*"
    return res

def transact_update(params):
    user_id = params['user_id']
    merchant_id = params['merchant_id']
    amount = float(params['amount'])
    timestamp = datetime.datetime.fromtimestamp(int(params['timestamp']))
    transaction_id = params['transaction_id']
    bank_id = params['bank_id']
    cashback = get_cashback(user_id, merchant_id)
    update_user(user_id, cashback, amount)
    update_vendor(cashback, amount)
    update_bank(cashback, amount)
    txn = Transaction(transaction_id=transaction_id,
                      timestamp=timestamp,
                      bank_id=bank_id,
                      user=User.objects.get(user_id=user_id),
                      merchant=Merchant.objects.get(merchant_id=merchant_id),
                      amount=amount,
                      cashback=cashback*amount)
    txn.save()
    update_message(user_id, cashback*amount)

def update_past_transaction(request):
    try:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(BASE_DIR, 'data/transaction.csv'), 'rb') as data_file:
            reader = csv.DictReader(data_file)
            for row in reader:
                params = {
                    'transaction_id': row['transaction_id'],
                    'user_id': row['unique_id'],
                    'merchant_id': row['merchant_id'],
                    'amount': row['amount'],
                    'timestamp': row['timestamp'],
                    'bank_id': row['bank_id']
                }    
                transact_update(params)
        response = {'success': True}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return JsonResponse(response)

def add_user_data():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(BASE_DIR, 'data/user_data.csv'), 'rb') as data_file:
        reader = csv.DictReader(data_file)
        for row in reader:
            user = User(user_id=row['unique_id'],
                        name=row['name'],
                        age=row['age'],
                        frequent_buyer=row['frequent'],
                        # customer_tag=row['income_tag'],
                        city=row['city'],
                        locality=row['locality'],
                        state=row['state']
                        )
            user.save()

def add_merchant_data():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(BASE_DIR, 'data/merchants.csv'), 'rb') as data_file:
        reader = csv.DictReader(data_file)
        for row in reader:
            merchant = Merchant(merchant_id=row['merchant_id'], name = row['merchant_name'])
            merchant.save()

def add_relevance_data(request):
    try:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(BASE_DIR, 'data/user_data.csv'), 'rb') as data_file:
            reader = csv.DictReader(data_file)
            for row in reader:
                if len(Relevance.objects.filter(user_id=row['unique_id'])) == 0:
                    rel = Relevance(user_id=row['unique_id'])                
                else:
                    rel = Relevance.objects.get(user_id=row['unique_id']) 
                rel.index = row['relevance']
                rel.save()
        response = {'success': True}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return JsonResponse(response)

def update_user(user_id, cashback, amount):
    user = User.objects.get(user_id=user_id)
    user.acc_balance = user.acc_balance - float(amount) + amount*cashback
    user.cashback_realized = amount * cashback
    user.save()

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
        user = User.objects.get(user_id=user_id)
        all_offer = Offer.objects.all()
        offer = all_offer[len(all_offer)-1]
        if int(merchant_id) == int(offer.merchant_id):
            cashback = offer.cashback
    except Exception as e:
        pass
    return cashback

def initialize(request):
    try:
        Vendor(id=0).save()
        Bank(id=0).save()
        add_merchant_data()
        add_user_data()
        response = {'success': True}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return JsonResponse(response)
        
def generate_offer(request):
    params = request.GET
    merchant_id = params['merchant_id']
    cashback = float(params['cashback'])/100
    goal_id = params['goal_id']
    # income_id = params['income_tag_id']
    # customer_tag_id = params['customer_tag_id']
    try:
        merchant = Merchant.objects.get(merchant_id=merchant_id)
        offer = Offer(merchant=merchant,
                      cashback=cashback,
                      goal=goal_id
                      # income_tag=income_id,
                      # customer_tag=customer_tag_id
                     )
        offer.save()
        save_messages(merchant_id, cashback)
        response = {'success': True}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    res = JsonResponse(response)
    res["Access-Control-Allow-Origin"] = "*"
    return res

def save_messages(merchant_id, cashback):
    merchant = Merchant.objects.get(merchant_id=merchant_id)
    message = 'Get ' + str(cashback * 100) + '% cashback on transaction at ' + merchant.name + '.'
    User.objects.all().update(message=message)

def update_message(user_id, cashback):
    message = 'Congrats you will get get your cashback of Rs. ' + str(cashback) + ' within 24 hrs.'
    User.objects.filter(user_id=user_id).update(message=message)
        
def get_relevance_data(request):
    data = {'user_id': [], 'index': []}
    try:
        relevance_data = Relevance.objects.all()
        for user in relevance_data:
            data['user_id'].append(user.user_id)
            data['index'].append(user.index)
        response = {'success': True, 'data': data}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return JsonResponse(response)

def get_transaction_data(request):
    merchant_id = request.GET['merchant_id']
    try:
        dates, sales, cashback = transaction_data(merchant_id)
        data = {
                'x': dates,
                'y': [{
                        'name': 'sales',
                        'data':  sales
                      },
                      {
                        'name': 'cashback',
                        'data':  cashback
                      }
                    ]
                }
        response = {'success': True, 'data': data}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return JsonResponse(response)

def transaction_data(merchant_id):
    txn_rows = Transaction.objects.filter(merchant_id=merchant_id).values()
    txn_data = defaultdict(lambda: defaultdict(int))
    for txn in txn_rows:
        date = txn['timestamp'].date()
        txn_data[date]['sales'] += txn['amount']
        txn_data[date]['cashback'] += txn['cashback']
    dates = sorted(txn_data)
    sales = [txn_data[date]['sales'] for date in dates]
    cashback = [txn_data[date]['cashback'] for date in dates]
    return dates, sales, cashback
