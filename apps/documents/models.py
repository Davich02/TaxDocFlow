from django.db import models
from apps.core.models import UniqueID,TimeStampedModel
from django.conf import settings
from apps.core.managers import SoftDeleteManager
from django.utils import timezone
from django.db.models import Q
from apps.users.models import Mandate




class Document(UniqueID, TimeStampedModel):
    class Status(models.TextChoices):
        UPLOADED = 'uploaded', 'Uploaded'
        OCR_DONE = 'ocr_done', 'OCR done'
        EXTRACTED = 'extracted', 'Extracted'
        NEEDS_REVIEW = 'needs_review', 'Needs review'
        CONFIRMED = 'confirmed', 'Confirmed'
        EXPORTED = 'exported', 'Exported'

    class Category(models.TextChoices):
        FAHRTKOSTEN = 'fahrtkosten', 'Fahrtkosten'
        ARBEITSMITTEL = 'arbeitsmittel', 'Arbeitsmittel'
        ARBEITSKLEIDUNG = 'arbeitskleidung', 'Arbeitskleidung'
        FORTBILDUNG = 'fortbildung', 'Fortbildung'
        GEWERKSCHAFT = 'gewerkschaft', 'Gewerkschaftsbeiträge'
        HOMEOFFICE = 'homeoffice', 'Homeoffice'
        BEWERBUNG = 'bewerbung', 'Bewerbungskosten'
        SONSTIGES = 'sonstiges', 'Sonstiges'

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name='documents_as_owner')
    file = models.FileField(upload_to='documents/%Y/%m/')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPLOADED)
    category = models.CharField(max_length=20, choices=Category.choices, blank=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    document_date = models.DateField(null=True,blank=True)
    vendor = models.CharField(max_length=255,blank=True)
    distance_km = models.DecimalField(null=True,blank=True,max_digits=10,decimal_places=2)
    raw_text = models.TextField(blank=True)
    ai_result = models.JSONField(blank=True,null=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    @classmethod
    def visible_to(cls, user):
        # id клиентов, с которыми у пользователя есть активный договор
        mandant_ids = Mandate.objects.filter(
            steuerberater=user, is_active=True
        ).values('mandant_id')
        return cls.objects.filter(Q(owner=user) | Q(owner_id__in=mandant_ids))


    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def __str__(self):
        return f"{self.vendor or 'Document'} ({self.status})"
