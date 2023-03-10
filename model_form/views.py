from django.http import HttpResponseRedirect
from django.shortcuts import render
from . forms import AuthorsForm
from django.contrib import messages


def author_create(request):
    if request.method == 'POST':
        form = AuthorsForm(request.POST)
        if form.is_valid():
            form_create = form.cleaned_data
            form_create = form.save(commit=False)
            form.save()
            messages.success(request, 'Все получилось')
    else:
        form = AuthorsForm()

    return render(request, 'model_form/author_form.html', {'form': form})
