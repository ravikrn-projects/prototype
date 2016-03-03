from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from prototype.models import Offers, Merchant, Vendor, Bank, User


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
