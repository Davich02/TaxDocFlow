import logging
from datetime import date
from decimal import Decimal

from .ai import extract_fields
from .models import Document
from .ocr import extract_text

logger = logging.getLogger(__name__)


def process_document(document):
    try:
        document.raw_text = extract_text(document.file.path)
        document.status = Document.Status.OCR_DONE
        document.save()
    except Exception:
        logger.exception('OCR failed for document %s', document.id)
        return

    try:
        data = extract_fields(document.raw_text)
    except Exception:
        logger.exception('AI extraction failed for document %s', document.id)
        return

    document.vendor = data.vendor or ''
    document.amount = Decimal(str(data.amount)) if data.amount is not None else None

    try:
        document.document_date = date.fromisoformat(data.document_date)
    except (TypeError, ValueError):
        document.document_date = None

    document.ai_result = data.model_dump()
    category = (data.category or '').lower()
    if category in Document.Category.values:
        document.category = category

    all_filled = all([document.vendor, document.amount, document.document_date, document.category])
    document.status = Document.Status.EXTRACTED if all_filled else Document.Status.NEEDS_REVIEW
    document.save()