import stripe
import requests
from rest_framework import status

from config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_product(product_data):
    """ Создание продукта в stripe """

    url = f'{settings.STRIPE_API_URL}/v1/products'
    headers = {'Authorization': f'Bearer {settings.STRIPE_SECRET_KEY}'}
    response = requests.post(url, headers=headers, json=product_data)

    if response.status_code == status.HTTP_201_CREATED:
        return response.json()
    else:
        return None


def create_price(price_data):
    """ Создание цены в stripe """

    url = f'{settings.STRIPE_API_URL}/v1/prices'
    headers = {'Authorization': f'Bearer {settings.STRIPE_SECRET_KEY}'}
    response = requests.post(url, headers=headers, json=price_data)

    if response.status_code == status.HTTP_201_CREATED:
        return response.json()
    else:
        return None


def create_checkout_session(price_id: str, success_url: str, cancel_url: str):
    """ Создание сессии оплаты в stripe """

    url = f'{settings.STRIPE_API_URL}/v1/checkout/sessions'
    headers = {'Authorization': f'Bearer {settings.STRIPE_SECRET_KEY}'}
    response = requests.post(url, headers=headers, json={
        'mode': 'payment',
        'payment_method_types': ['card'],
        'line_items': [{
            'price': price_id,
            'quantity': 1,
        }],
        'success_url': success_url,
        'cancel_url': cancel_url,
    })
    # success_url и cancel_url - адреса, на которые stripe будет перенаправлять пользователя
    # в случае успешной или отмененной оплаты, соответственно

    if response.status_code == status.HTTP_201_CREATED:
        return response.json()
    else:
        return None
