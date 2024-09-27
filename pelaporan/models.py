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
    

KOTA_CHOICES = [
    ('Palembang', 'Palembang'),
    ('Bengkulu', 'Bengkulu'),
    ('Bandar Lampung', 'Bandar Lampung'),
    ('Pangkal Pinang', 'Pangkal Pinang'),
    ('Padang', 'Padang'),
    ('Pekanbaru', 'Pekanbaru'),
    ('Jambi', 'Jambi'),
    ('Batam', 'Batam'),
    ('Medan', 'Medan'),
    ('Banda Aceh', 'Banda Aceh'),
    ('Surabaya', 'Surabaya'),
    ('Semarang', 'Semarang'),
    ('Yogyakarta', 'Yogyakarta'),
    ('Bandung', 'Bandung'),
    ('Serang', 'Serang'),
    ('Jakarta', 'Jakarta'),
    ('Banjarmasin', 'Banjarmasin'),
    ('Samarinda', 'Samarinda'),
    ('Palangkaraya', 'Palangkaraya'),
    ('Pontianak', 'Pontianak'),
    ('Tarakan', 'Tarakan'),
    ('Makassar', 'Makassar'),
    ('Manado', 'Manado'),
    ('Palu', 'Palu'),
    ('Kendari', 'Kendari'),
    ('Mamuju', 'Mamuju'),
    ('Ambon', 'Ambon'),
    ('Jayapura', 'Jayapura'),
    ('Manokwari', 'Manokwari'),
    ('Gorontalo', 'Gorontalo'),
    ('Ternate', 'Ternate'),
    ('Denpasar', 'Denpasar'),
    ('Mataram', 'Mataram'),
    ('Kupang', 'Kupang'),
    ('Cirebon', 'Cirebon'),
    ('Lhokseumawe', 'Lhokseumawe'),
    ('Pematang Siantar', 'Pematang Siantar'),
    ('Sibolga', 'Sibolga'),
    ('Malang', 'Malang'),
    ('Kediri', 'Kediri'),
    ('Jember', 'Jember'),
    ('Solo', 'Solo'),
    ('Purwokerto', 'Purwokerto'),
    ('Tegal', 'Tegal'),
    ('Tasikmalaya', 'Tasikmalaya'),
    ('Balikpapan', 'Balikpapan'),
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
    kota = models.CharField(max_length=50, choices=KOTA_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='review')
    tanggal_pengerjaan = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='laporan_images/', null=True, blank=True)

    def __str__(self):
        return f"Laporan {self.id} - {self.jenis_kerusakan}"


