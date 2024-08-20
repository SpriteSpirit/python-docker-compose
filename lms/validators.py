from rest_framework.serializers import ValidationError


class UrlValidator:
    """ Проверка валидности ссылок """

    def __init__(self, url):
        self.url: str = url

    def __call__(self, value: str):
        """ Проверка, что URL содержит ссылку на YouTube """

        if value:
            if 'www.youtube.com' not in value:
                raise ValidationError('Ссылка должна быть только на youtube.com')
