from rest_framework import generics
from rest_framework.permissions import AllowAny

from .permissions import IsSteuerberater
from .serializers import RegisterSerializer, UserSerializer, MandateSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Mandate


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user




class MandateListCreateView(generics.ListCreateAPIView):
    serializer_class = MandateSerializer
    permission_classes = [IsAuthenticated,IsSteuerberater]

    def get_queryset(self):
        return Mandate.objects.filter(steuerberater=self.request.user)

    def perform_create(self, serializer):
        serializer.save(steuerberater=self.request.user)
