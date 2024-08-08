import json

from django.core.management import BaseCommand

from users.models import Payment


class Command(BaseCommand):
    help = 'Заполнение базы данными из JSON-файлов'

    @staticmethod
    def json_read_payments(json_file_name):
        payments = []

        # Здесь мы получаем данные из фикстур с оплатами
        with open(json_file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                if item.get('model') == "users.payment":
                    print(item.get('model'))
                    payments.append(item)

        return payments

    def handle(self, *args, **options):
        # Удаление всех оплат
        Payment.objects.all().delete()
        # Имя JSON файла
        json_name = "data_base.json"

        payments_for_create = []

        for payment in Command.json_read_payments(json_name):
            payments_for_create.append(Payment(**payment))

        Payment.objects.bulk_create(payments_for_create)
