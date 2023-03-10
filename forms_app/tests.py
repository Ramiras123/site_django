from django.test import Client, TestCase
from forms_app.forms import ContactForm
import pytest
from django import forms
from datetime import datetime, timedelta
from django.urls import reverse

MAX_LENGTH_499 = 'n' * 499
MAX_LENGTH_99 = '0' * 99
MAX_LENGTH_501 = 'n' * 501
MAX_LENGTH_101 = 'n' * 101


@pytest.mark.parametrize(
    'date_creation, valid_date',
    [
        #  дата сегодня
        (datetime.today(), True),
        # Проверка метода clean
        ('2021-02-12', False),
        ('2030-02-12', False),
        # Невозможные значения
       (None, False),
        ('', False)
    ]
)
@pytest.mark.parametrize(
    'subject, valid_subject',
    [
        # Истинное заполнение заголовка
        ('Заголовок', True),
        # проверка максимальных символов
        (MAX_LENGTH_99, True),
        (MAX_LENGTH_101, False),
        # Невозможные значения
        ('', False),
        (None, False)
    ]
)
@pytest.mark.parametrize(
    'message, valid_message',
    [
        # Истинное заполнение сообщения
        ('dasdasd asda sdasdasd', True),
        #проверка максимальных символов
        (MAX_LENGTH_499, True),
        (MAX_LENGTH_501, False),
        # Невозможные значения
        ('', False),
        (None, False)
    ]
)
@pytest.mark.parametrize(
    'sender, valid_sender',
    [
        ('admin@mail.com', True),
        # Невозможные значения
        ('@mail.ru', False),
        ('da', False),
        ('', False),
        (None, False)
    ]
)
@pytest.mark.parametrize(
    'cc_myself, valid_myself',
    [
        ('1', True),
  #      (None, False)
    ]
)
def test_contact_form_valid(date_creation, subject, message, sender, cc_myself, valid_date, valid_subject,
                            valid_message, valid_sender, valid_myself):
    test_form = ContactForm(
        data={
            "subject": subject,
            "message": message,
            "sender": sender,
            "cc_myself": cc_myself,
            "date_creation": date_creation})
    form_error = test_form.errors.as_data()
    print(form_error)
    assert test_form.is_valid() is (valid_date and
                                    valid_subject and
                                    valid_message and
                                    valid_sender and
                                    valid_myself)


