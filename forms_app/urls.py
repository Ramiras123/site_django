from django.urls import path, include
from . views import contact_send, success_send
app_name = 'form'
urlpatterns = [
    path('contact/', contact_send, name='contact'),
    path('success/', success_send, name='success'),
]