# Generated by Django 3.0.6 on 2020-06-11 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0004_auto_20200611_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, upload_to='MEDIA_COMPANY_IMAGE_DIR'),
        ),
    ]
