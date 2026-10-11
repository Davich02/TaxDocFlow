from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'owner', 'category', 'amount', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('vendor', 'owner__email')
    exclude = ('deleted_at',)