# Generated by Django 5.1.1 on 2024-09-26 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pelaporan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='laporankerusakan',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='laporan_images/'),
        ),
    ]
