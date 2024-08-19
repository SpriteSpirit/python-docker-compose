from rest_framework.serializers import ValidationError
import re


class UrlValidator:
    """ Проверка валидности ссылок """

    def __init__(self, url):
        self.url: str = url

    def __call__(self, value: str):
        """ Проверка, что URL содержит ссылку на YouTube """

        reg_ex = re.compile(r"^https?://(?:www\.)?youtube\.com/.*$")
        temp_value = dict(value).get(self.url)

        if not bool(reg_ex.match(temp_value)):
            raise ValidationError('Ссылка должна быть только на youtube.com')
        return value
