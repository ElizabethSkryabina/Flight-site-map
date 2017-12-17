from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^flights/$', views.flights, name='flights'),
    url(r'^ajax/validate_airport/$', views.validate_airport, name='validate_airport')
]