from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from prototype.models import Offers, Merchant


def index(request):
    return HttpResponse("Hello, world.")


def generate_offers(request):
	params = request.GET
	offer = Offers.objects.filter(id=2)[0]
	merchant_id = offer.merchant_id
	merchant_name = Merchant.objects.filter(id = merchant_id)[0].name
	response = {'merchant': merchant_name, 'cashback': offer.cashback, 
				'cashback_status': offer.cashback_status}
	return JsonResponse(response)


