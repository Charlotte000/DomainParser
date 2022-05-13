from django.urls import path

from domainparser.views import index

urlpatterns = [
    path('', index)
]
