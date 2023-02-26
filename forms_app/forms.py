from django import forms
from datetime import date, timedelta

from django.forms import DateInput


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(max_length=500)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=True)
    date_creation = forms.DateField(initial=date.today)

    def clean_date_creation(self):
        date_new = self.cleaned_data['date_creation']
        if date_new != date.today():
            raise forms.ValidationError('Форма не действительная')
        return date_new
