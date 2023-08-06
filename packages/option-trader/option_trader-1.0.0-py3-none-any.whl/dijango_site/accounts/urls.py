from django.urls import path

from . import views

urlpatterns = [
    path("", views.IB_conntect, name="IB connect"),         
]
