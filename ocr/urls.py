from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ocr.views import (
    upload_invoice,
    export_to_csv,
    get_invoices,
    get_extracted_data,
    list_files,
    delete_file,
)

urlpatterns = [
    path("upload/", upload_invoice, name="upload_invoice"),
    path("export/", export_to_csv, name="export_to_csv"),
    path("invoices/", get_invoices, name="get_invoices"),
    path("list_files/", list_files, name="list_files"),
    path(
        "delete_file/<str:file_type>/<str:filename>/", delete_file, name="delete_file"
    ),
    path(
        "extracted_data/<int:invoice_id>/",
        get_extracted_data,
        name="get_extracted_data",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

print("✅ ルーティング設定が完了しました！")
