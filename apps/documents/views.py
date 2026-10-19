from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Document
from .serializers import DocumentSerializer



class DocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Document.visible_to(self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

