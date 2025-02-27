from django.conf import settings
import unicodedata
import re
import csv
import os

# import boto3
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import default_storage
from .models import Invoice, ExtractedData
from django.core.files.base import ContentFile

# from .utils import process_invoice_with_textract  # Textract を使用
from .serializers import InvoiceSerializer, ExtractedDataSerializer
from django.http import HttpResponse
from pypdf import PdfReader
from .models import UploadedFile
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from rest_framework.decorators import api_view

POPPLER_PATH = "/opt/homebrew/bin/"


@api_view(["GET"])
def list_files(request):
    """media/uploads と media/csv 内のファイル一覧を取得するAPI"""
    pdf_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
    csv_dir = os.path.join(settings.MEDIA_ROOT, "csv")

    pdf_files = os.listdir(pdf_dir) if os.path.exists(pdf_dir) else []
    csv_files = os.listdir(csv_dir) if os.path.exists(csv_dir) else []

    return JsonResponse({"pdf_files": pdf_files, "csv_files": csv_files}, status=200)


@api_view(["DELETE"])
def delete_file(request, file_type, filename):
    """指定されたファイルを削除する"""
    if file_type not in ["pdf", "csv"]:
        return JsonResponse({"error": "Invalid file type"}, status=400)

    # ファイルの保存ディレクトリを決定
    file_dir = os.path.join(
        settings.MEDIA_ROOT, "uploads" if file_type == "pdf" else "csv"
    )
    file_path = os.path.join(file_dir, filename)

    # ファイルの存在をチェックして削除
    if os.path.exists(file_path):
        os.remove(file_path)
        return JsonResponse({"message": f"{filename} を削除しました"}, status=200)
    else:
        return JsonResponse({"error": "ファイルが見つかりません"}, status=404)


@api_view(["GET"])
def get_invoices(request):
    invoices = Invoice.objects.all()
    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_extracted_data(request, invoice_id):
    extracted_data = ExtractedData.objects.filter(invoice_id=invoice_id)
    serializer = ExtractedDataSerializer(extracted_data, many=True)
    return Response(serializer.data)


def sanitize_filename(filename):
    """日本語・特殊文字を安全なファイル名に変換"""
    filename = unicodedata.normalize("NFKD", filename)
    filename = re.sub(r"[^\w\-_\.]", "_", filename)  # 不正な文字を置換
    return filename


@csrf_exempt
def upload_invoice(request):
    print("✅ POSTリクエストを受信")  # デバッグ用ログ

    if request.method == "POST":
        print(f"📂 request.FILES: {request.FILES}")  # デバッグ用ログ

        if "invoice" not in request.FILES:
            print("❌ 'invoice' がリクエストに含まれていません")
            return JsonResponse({"error": "No file uploaded"}, status=400)

        uploaded_file = request.FILES["invoice"]
        print(f"✅ ファイル受信: {uploaded_file.name}")

        # ✅ media/uploads/ に保存
        save_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, uploaded_file.name)

        with open(save_path, "wb+") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        print(f"✅ ファイル保存完了: {save_path}")

        # ✅ PDF → テキスト抽出
        extracted_text = extract_text_from_pdf(save_path)
        if not extracted_text:
            print("❌ OCR に失敗しました")
            return JsonResponse({"error": "Failed to extract text"}, status=500)

        # ✅ CSV に変換して保存
        csv_filename = uploaded_file.name.replace(".pdf", ".csv")
        csv_dir = os.path.join(settings.MEDIA_ROOT, "csv")
        os.makedirs(csv_dir, exist_ok=True)
        csv_path = os.path.join(csv_dir, csv_filename)

        save_text_to_csv(extracted_text, csv_path)

        print(f"✅ CSV 変換完了: {csv_path}")

        return JsonResponse(
            {
                "message": "File uploaded and converted to CSV successfully",
                "filename": uploaded_file.name,
                "csv_filename": csv_filename,
            },
            status=200,
        )

    return JsonResponse({"error": "Invalid request"}, status=400)


# @csrf_exempt
# def upload_invoice(request):
#     if request.method == "POST" and request.FILES.get("invoice"):
#         uploaded_file = request.FILES["invoice"]

#         # AWS S3 にアップロード
#         s3_client = boto3.client("s3", region_name="ap-northeast-1")
#         s3_bucket = "your-s3-bucket-name"
#         s3_key = f"invoices/{uploaded_file.name}"

#         s3_client.upload_fileobj(uploaded_file, s3_bucket, s3_key)

#         invoice = Invoice.objects.create(file_path=s3_key)

#         # AWS Textract でOCR解析
#         extracted_text = process_invoice_with_textract(s3_bucket, s3_key)

#         ExtractedData.objects.create(
#             invoice=invoice, field_name="raw_text", field_value=extracted_text
#         )

#         return JsonResponse(
#             {
#                 "message": "File uploaded, processed with Textract, and stored successfully."
#             }
#         )

#     return JsonResponse({"error": "Invalid request."}, status=400)


def export_to_csv(request):
    invoices = Invoice.objects.all()
    response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
    response["Content-Disposition"] = 'attachment; filename="invoices.csv"'

    writer = csv.writer(response)
    writer.writerow(
        [
            "発行日",
            "請求番号",
            "発行元",
            "発行者",
            "住所",
            "電話番号",
            "メールアドレス",
            "登録番号",
            "請求先",
            "件名",
            "品名",
            "数量",
            "単価",
            "小計",
            "消費税",
            "合計",
            "銀行名",
            "支店名",
            "口座番号",
            "口座名義",
        ]
    )

    for invoice in invoices:
        extracted_data = ExtractedData.objects.filter(invoice=invoice)
        row = [
            invoice.issue_date,
            invoice.invoice_number,
            invoice.company_name,
            invoice.issuer_name,
            invoice.address,
            invoice.phone,
            invoice.email,
            invoice.registration_number,
            invoice.client_name,
            invoice.subject,
            None,
            None,
            None,
            None,
            None,
            None,
            invoice.bank_name,
            invoice.branch_name,
            invoice.account_number,
            invoice.account_holder,
        ]
        for data in extracted_data:
            row[10] = data.field_name
            row[11] = data.quantity
            row[12] = data.unit_price
            row[13] = data.subtotal
            row[14] = data.tax
            row[15] = data.total
            writer.writerow(row)

    return response


# def extract_text_from_pdf(pdf_path):
#     """
#     PDF からテキストを抽出する関数
#     """
#     text = []
#     with open(pdf_path, "rb") as pdf_file:
#         reader = PdfReader(pdf_file)
#         for page in reader.pages:
#             text.append(page.extract_text())
#     return "\n".join(text)
def extract_text_from_pdf(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)

    # 1️⃣ PyPDFでテキストを抽出（テキストデータがある場合）
    for page in reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text + "\n"

    # 2️⃣ PyPDFでテキストが取れなかった場合、OCRを実行
    if not text.strip():
        print("📸 PDF にテキストデータがないため、OCRを実行します...")
        images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)

        for i, image in enumerate(images):
            # 画像をOCR処理
            ocr_text = pytesseract.image_to_string(
                image, lang="eng+jpn"
            )  # 日本語と英語を認識
            text += ocr_text + "\n"

    return text.strip()


def save_text_to_csv(text, csv_path):
    """
    抽出したテキストを CSV に保存する関数
    """
    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        for line in text.split("\n"):
            writer.writerow([line])
