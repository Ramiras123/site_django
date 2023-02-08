from django import forms
import datetime


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(max_length=500)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    date_creation = forms.DateField(help_text='Заполнить форму не позднее 1 недели')

    def clean_date_creation(self):
         data = self.cleaned_data['date_creation']
         if data < datetime.date.today():
             raise forms.ValidationError('Форма не действительная')
