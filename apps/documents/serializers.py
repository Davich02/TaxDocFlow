import os

from rest_framework import serializers
from .models import Document

MAX_FILE_SIZE = 1024 * 1024 * 10
ALLOWED_EXTENSIONS = ['.pdf', '.jpeg', '.png','.jpg']


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'file', 'status', 'category', 'amount', 'document_date', 'vendor', 'distance_km', 'created_at']
        read_only_fields = ['id', 'status', 'category', 'amount', 'document_date', 'vendor', 'distance_km', 'created_at']


    def validate_file(self, value):
        if value.size > MAX_FILE_SIZE:
            raise serializers.ValidationError('File size must be less than 10MB.')
        if os.path.splitext(value.name)[1].lower() not in ALLOWED_EXTENSIONS:
            raise serializers.ValidationError('File type must be one of: .pdf, .jpeg, .png, .jpg.')
        return value