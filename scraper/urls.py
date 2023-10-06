from django.urls import path

from . import views
urlpatterns = [
    path('', views.get_data, name='get_data'),
    path('contact_us/', views.contact_us, name='contactus'),
    ]