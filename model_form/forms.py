from . models import Author, Book, TITLE_CHOICES
from django import forms


class AuthorForm(forms.ModelForm):
    model = Author
    fields = ['name', 'birth_date', 'title']


class BookForm(forms.ModelForm):
    model = Book
    fields = ['name', 'author']


class AuthorsForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('name', 'birth_date', 'title')
        widgets = {
            "name": forms.Textarea(attrs={'cols': 80, 'rows': 20})
        }

"""
class AuthorsForm(forms.Form):
    name = forms.CharField(max_length=100)
    title = forms.CharField(max_length=3,
                            widget=forms.Select(choices=TITLE_CHOICES))
    birth_day = forms.DateField(required=False)
"""


class BooksForm(forms.Form):
    name = forms.CharField(max_length=100)
    author = forms.ModelMultipleChoiceField(queryset=Author.objects.all())
