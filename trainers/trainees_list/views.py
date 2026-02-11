from .serializers import registrationSerializers
from .models import Registration
from rest_framework import generics

class trainee_registration(generics.CreateAPIView):
    serializer_class = registrationSerializers
    queryset = Registration.objects.all()
    authentication_classes = []
    permission_classes = []