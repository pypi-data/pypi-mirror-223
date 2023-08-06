from abc import abstractmethod
from importlib import import_module
from inspect import getmembers, isclass
from typing import Type

from django.conf import settings
from django.contrib.auth import get_user_model
from django.template import Template
from mail_satvadev.messages import BaseMail
from mail_satvadev.tasks import send_email

from auth_satvadev.api.exceptions import CodeDoesNotMatchError
from auth_satvadev.models import VerificationCode


class BaseCodeSender:
    """Базовый класс для отправки и проверки кода подтверждения"""

    @abstractmethod
    def send_code(self, code: int, data: dict):
        """Метод для отправки кода с использованием указанного в запросе
        способа связи
        """
        raise NotImplementedError(
            f'Method send_code not implemented in {self.__class__.__name__}')

    @abstractmethod
    def validate_code(self, data: dict):
        """Метод для валидации кода в запросе для выбранного способа связи"""
        raise NotImplementedError(
            f'Method validate_code not implemented in '
            f'{self.__class__.__name__}'
        )


class MailSender(BaseCodeSender):
    """Класс для отправки по email и проверки кода подтверждения"""

    class ResetPasswordMail(BaseMail):
        """Класс генерирует текст письма с проверочным кодом"""
        subject_template = Template('Сброс пароля')
        template = Template('Проверочный код: {{ code }}')

    def send_code(self, code: int, data: dict):
        """Метод для отправки кода на указанный в запросе email"""
        email = [data.get('email')]
        mail = self.ResetPasswordMail(code=code)
        send_email.delay(mail.subject, email, mail.text)

    def validate_code(self, data: dict):
        """Метод для валидации кода в запросе для email"""
        input_code = data.get('code')
        email = data.get('email')
        verification = VerificationCode.objects.get(user__email=email)

        if input_code != verification.code:
            raise CodeDoesNotMatchError

        verification.delete()

        return get_user_model().objects.get(email=email)


def get_sender_class() -> Type[BaseCodeSender]:
    """Метод для определения класса для отправки и валидации кодов
    подтверждения

    Возвращает только наследуемые от BaseCodeSender классы
    """
    # TODO: добавить возможность использования нескольких классов для отправки
    # TODO: сообщений с кодом подтверждения
    sender_settings = getattr(
        settings,
        'SENDER_CLASS',
        'auth_satvadev.senders.MailSender',
    ).split('.')
    sender_module = import_module('.'.join(sender_settings[:-1]))

    sender_classes = [
        class_
        for class_name, class_ in getmembers(sender_module, isclass)
        if (
            class_name == sender_settings[-1] and
            issubclass(class_, BaseCodeSender)
        )
    ]

    if len(sender_classes) == 0:
        raise ValueError('Sender classes not found')

    return sender_classes[0]
