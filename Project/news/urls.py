from django.urls import path

import news
from .views import index, test

urlpatterns = [
    path('', index),
    path('test/', test),
]