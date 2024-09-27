from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('requester', 'Requester'),
        ('approver', 'Approver & Scheduler'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
    

PROVINSI_CHOICES = [
    ('Aceh', 'Aceh'),
    ('Bali', 'Bali'),
    ('Banten', 'Banten'),
    ('Bengkulu', 'Bengkulu'),
    ('DI Yogyakarta', 'DI Yogyakarta'),
    ('DKI Jakarta', 'DKI Jakarta'),
    ('Gorontalo', 'Gorontalo'),
    ('Jambi', 'Jambi'),
    ('Jawa Barat', 'Jawa Barat'),
    ('Jawa Tengah', 'Jawa Tengah'),
    ('Jawa Timur', 'Jawa Timur'),
    ('Kalimantan Barat', 'Kalimantan Barat'),
    ('Kalimantan Selatan', 'Kalimantan Selatan'),
    ('Kalimantan Tengah', 'Kalimantan Tengah'),
    ('Kalimantan Timur', 'Kalimantan Timur'),
    ('Kalimantan Utara', 'Kalimantan Utara'),
    ('Kepulauan Bangka Belitung', 'Kepulauan Bangka Belitung'),
    ('Kepulauan Riau', 'Kepulauan Riau'),
    ('Lampung', 'Lampung'),
    ('Maluku', 'Maluku'),
    ('Maluku Utara', 'Maluku Utara'),
    ('Nusa Tenggara Barat', 'Nusa Tenggara Barat'),
    ('Nusa Tenggara Timur', 'Nusa Tenggara Timur'),
    ('Papua', 'Papua'),
    ('Papua Barat', 'Papua Barat'),
    ('Riau', 'Riau'),
    ('Sulawesi Barat', 'Sulawesi Barat'),
    ('Sulawesi Selatan', 'Sulawesi Selatan'),
    ('Sulawesi Tengah', 'Sulawesi Tengah'),
    ('Sulawesi Tenggara', 'Sulawesi Tenggara'),
    ('Sulawesi Utara', 'Sulawesi Utara'),
    ('Sumatera Barat', 'Sumatera Barat'),
    ('Sumatera Selatan', 'Sumatera Selatan'),
    ('Sumatera Utara', 'Sumatera Utara'),
]

# Custom User Model to handle different roles
class LaporanKerusakan(models.Model):
    STATUS_CHOICES = (
        ('review', 'Sedang di review'),
        ('rejected', 'Rejected'),
        ('approved', 'Approved'),
    )

    KERUSAKAN_CHOICES = (
        ('listrik', 'Listrik'),
        ('air', 'Air'),
        ('kamar_mandi', 'Kamar Mandi'),
        ('furniture', 'Furniture'),
        ('bocor', 'Bocor'),
    )

    TINGKAT_KERUSAKAN_CHOICES = (
        ('kecil', 'Kecil'),
        ('sedang', 'Sedang'),
        ('besar', 'Besar'),
    )

    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    alamat = models.TextField()
    jenis_kerusakan = models.CharField(max_length=20, choices=KERUSAKAN_CHOICES)
    tingkat_kerusakan = models.CharField(max_length=10, choices=TINGKAT_KERUSAKAN_CHOICES)
    deskripsi = models.TextField()
    provinsi = models.CharField(max_length=50, choices=PROVINSI_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='review')
    tanggal_pengerjaan = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='laporan_images/', null=True, blank=True)

    def __str__(self):
        return f"Laporan {self.id} - {self.jenis_kerusakan}"


