import requests, json

import ipdb
#ipdb.set_trace()
data_file = open('data/tr.csv', 'w')
for transaction in data_file:
	params = {
			'user_id': transaction['user_id'], 
			'merchant_id': transaction['merchant_id'],
			'amount': transaction['amount']
			}
	requests.get('localhost:8000/cardbytes/transact', params = params)


