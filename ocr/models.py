from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)


class Invoice(models.Model):
    issue_date = models.DateField(null=True, blank=True)  # NULL 許可
    invoice_number = models.CharField(
        max_length=100, null=True, blank=True
    )  # NULL 許可
    company_name = models.CharField(max_length=255, null=True, blank=True)
    issuer_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)  # 修正
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    registration_number = models.CharField(max_length=50, null=True, blank=True)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    bank_name = models.CharField(max_length=255, null=True, blank=True)  # 修正
    branch_name = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=50, null=True, blank=True)  # 修正
    account_holder = models.CharField(max_length=255, null=True, blank=True)  # 修正


class ExtractedData(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=255)
    quantity = models.IntegerField(null=True, blank=True)  # NULL許可
    unit_price = models.IntegerField(null=True, blank=True)
    subtotal = models.IntegerField(null=True, blank=True)
    tax = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)


class CSVExport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    export_date = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=500)


class UploadedFile(models.Model):
    file_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to="uploads/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
