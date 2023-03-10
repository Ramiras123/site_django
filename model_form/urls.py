from django.urls import path
from . views import author_create
app_name = 'model_form'
urlpatterns = [
    path('author/create/', author_create, name='author-create'),

]