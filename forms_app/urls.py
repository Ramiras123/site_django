from django.urls import path, include
from . views import contact_send, send_success
app_name = 'form'
urlpatterns = [
    path('contact/', contact_send, name='contact'),
    path('success/', send_success, name='success'),
]