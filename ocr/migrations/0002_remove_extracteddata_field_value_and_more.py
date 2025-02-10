# Generated by Django 4.2.19 on 2025-02-10 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extracteddata',
            name='field_value',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='file_path',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='status',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='upload_date',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='user',
        ),
        migrations.AddField(
            model_name='extracteddata',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='extracteddata',
            name='subtotal',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='extracteddata',
            name='tax',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='extracteddata',
            name='total',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='extracteddata',
            name='unit_price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='account_holder',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='account_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='bank_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='branch_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='client_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='company_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='issue_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='issuer_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='registration_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='subject',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
