from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from prototype.models import Offers, Merchant


def index(request):
    return HttpResponse("Hello, Welocome to Cardbytes Prototype.")

def generate_offers(request):
	params = request.GET
	offer = Offers.objects.filter(id=2)[0]
	merchant_id = offer.merchant_id
	merchant_name = Merchant.objects.filter(id = merchant_id)[0].name
	response = {'merchant': merchant_name, 'cashback': offer.cashback, 
				'cashback_status': offer.cashback_status}
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
