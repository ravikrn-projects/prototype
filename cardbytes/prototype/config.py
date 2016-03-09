vendor_commission = 0.1
bank_commission = 0.02
bank_commission_clm = 0.05

income_tag = [
             {"name": "High Paying", "id": 0},
             {"name": "Low Paying", "id": 1},
]

customer_tag = [
             {"name": "Fashion", "id": 0},
             {"name": "Ecommerce", "id": 1},
             {"name": "Restaurant", "id": 1},
             {"name": "Travel", "id": 1}
]

goals = [
             {"name": "Loyalty program", "id": 0},
             {"name": "New customer acquisition", "id": 1}
]

base_url = "http://localhost:8000/cardbytes/"

urls = {
        'get_relevance_data': base_url + 'get_relevance_data',
        'show_offers': base_url + 'show_offers',
        'get_bank_revenue': base_url + 'get_bank_revenue',
        'get_vendor_revenue': base_url + 'get_vendor_revenue',
        'get_transaction_data': base_url + 'get_transaction_data',
        'transact': base_url + 'transact',
        'user': base_url + 'user',
        'get_merchants': base_url + 'get_merchants',
        'generate_offer': base_url + 'generate_offer'
}
