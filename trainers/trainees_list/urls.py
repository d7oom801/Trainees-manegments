from django.urls import path
from .views import trainee_registration
urlpatterns = [
    path('registration', trainee_registration.as_view(), name='registration')


]
