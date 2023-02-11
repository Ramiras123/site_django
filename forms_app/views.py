from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from forms_app.forms import ContactForm
from django.contrib import messages
from django.http import HttpResponse


def contact_send(request):
    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            date_creation = form.cleaned_data['date_creation']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
            recipients = ['smirnow201494@gmail.com']
            if cc_myself:
                recipients.append(message)
            try:
                send_mail(subject, message, sender, recipients)
            except BadHeaderError:
                return HttpResponse('Что то пошло не так')
            return redirect('form:success')
        else:
            messages.error(request, "error")
    return render(request, 'forms_app/email.html', {'form': form})


def send_success(request):
    return HttpResponse('ваше сообщение доставлено')
