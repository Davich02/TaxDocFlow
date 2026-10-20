from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Document
from .ocr import extract_text
from .serializers import DocumentSerializer
import logging

logger = logging.getLogger(__name__)



class DocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Document.visible_to(self.request.user)

    def perform_create(self, serializer):
        document = serializer.save(owner=self.request.user)
        try:
            document.raw_text = extract_text(document.file.path)
            document.status = Document.Status.OCR_DONE
            document.save()
        except Exception:
            logger.exception('ORC failed for document',document.id)



class DocumentDetailView(generics.RetrieveAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return Document.visible_to(self.request.user)
