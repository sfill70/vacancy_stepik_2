# Generated by Django 3.0.6 on 2020-06-12 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0005_auto_20200611_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, upload_to='company_images'),
        ),
    ]
