from django.urls import path
from .views import upload_invoice, export_to_csv
from .views import get_invoices, get_extracted_data
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("upload/", upload_invoice, name="upload_invoice"),
    path("export/", export_to_csv, name="export_to_csv"),
    path("invoices/", get_invoices, name="get_invoices"),
    path(
        "extracted_data/<int:invoice_id>/",
        get_extracted_data,
        name="get_extracted_data",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
