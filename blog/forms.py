from django import forms
from django.forms import fields, widgets
from . models import Comment


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control custom-text',
                                                        'cols': '40',
                                                        'rows': '4'}),
                           label='Текст сообщения')

    class Meta:
        model = Comment
        fields = ['body',]