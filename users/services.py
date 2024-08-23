from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_price(product_id, price):
    """ Создает цену в Stripe """
    return stripe.Price.create(
        currency="rub",
        unit_amount=int(price * 100),
        product=product_id,
    )


def create_stripe_product(product_name):
    """ Создает товар в Stripe """
    product = stripe.Product.create(
        name=product_name
    )

    return product


def create_stripe_session(price):
    """ Создает сессию для оплаты в Stripe """
    session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8001/users/success_url',
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url


# def get_stripe_session_data(session_id):
#     """Получает данные о сессии Stripe по идентификатору."""
#     try:
#         session = stripe.checkout.Session.retrieve(session_id)
#         return session
#     except stripe.error.InvalidRequestError as e:
#         # Обработка ошибки, если сессия не найдена
#         print(f"Ошибка Stripe: {e}")
#         return None
#

def get_checkout_session_status(session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session
    except Exception as e:
        return str(e)
