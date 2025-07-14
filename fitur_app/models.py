# checkup/models.py

from django.db import models
from cloudinary.models import CloudinaryField  # Import CloudinaryField

from alamat_app.models import Desa
from hash_app.utils import generate_unique_hash


class CheckupCategory(models.Model):
    # Kategori yang dapat dimasukkan secara dinamis
    nama_kategori = models.CharField(max_length=255, unique=True)
    content_hash = models.CharField(max_length=64, editable=False, null=True, blank=True)

    def __str__(self):
        return self.nama_kategori

    def save(self, *args, **kwargs):
        # Generate a new unique hash (using timestamp)
        self.content_hash = generate_unique_hash()  # Use the unique hash generator

        super().save(*args, **kwargs)


class Feature(models.Model):
    kategori = models.ForeignKey(CheckupCategory, null=True, blank=True, related_name='fitur', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = CloudinaryField('image', null=True, blank=True)  # Tambahkan field image
    min_age_in_days = models.IntegerField(null=True, blank=True, help_text="Minimum age in days")  # Minimum age in days
    max_age_in_days = models.IntegerField(null=True, blank=True, help_text="Maximum age in days")
    initial_instructions = models.TextField(null=True, blank=True)
    final_instructions = models.TextField(null=True, blank=True)
    requires_analysis = models.BooleanField(default=False,
                                            help_text="Indicates whether this feature requires analysis")  # Defaultnya tidak membutuhkan analisis
    content_hash = models.CharField(max_length=64, editable=False, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate a new unique hash (using timestamp)
        self.content_hash = generate_unique_hash()  # Use the unique hash generator

        super().save(*args, **kwargs)



from django.db import models
from datetime import datetime, date

from datetime import datetime
from dateutil.relativedelta import relativedelta

class CheckupGroup(models.Model):
    JENIS_KELAMIN_CHOICES = [
        ('L', 'Laki-Laki'),
        ('P', 'Perempuan'),
    ]
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Relasi dengan pengguna
    kategori = models.ForeignKey(CheckupCategory, on_delete=models.CASCADE)  # Kategori pengecekan
    hpht = models.DateField(help_text="Hari Pertama Haid Terakhir", null=True, blank=True)
    nama = models.CharField(max_length=255, null=True, blank=True)
    tanggal_lahir = models.DateField(help_text="Tanggal lahir pengguna", null=True, blank=True)
    jenis_kelamin = models.CharField(max_length=1, choices=JENIS_KELAMIN_CHOICES, null=True, blank=True)
    nik = models.CharField(max_length=16, null=True, blank=True)  # NIK untuk pengguna dewasa
    nama_ibu = models.CharField(max_length=255, null=True, blank=True)  # Nama ibu untuk bayi
    nik_ibu = models.CharField(max_length=16, null=True, blank=True)  # NIK ibu untuk bayi
    foto = CloudinaryField('image', null=True, blank=True)  # Tambahkan field image
    tanggal_pendaftaran = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)  # 🟢 Soft delet
    desa = models.ForeignKey(Desa, on_delete=models.CASCADE, null=True, blank=True)
    content_hash = models.CharField(max_length=64, editable=False, null=True, blank=True)

    def hitung_umur_hari(self):
        """Menghitung umur dalam hari berdasarkan tanggal lahir."""
        if self.tanggal_lahir:
            umur_hari = (datetime.now().date() - self.tanggal_lahir).days
            return umur_hari
        return None

    def get_umur_terformat(self):
        """Mengembalikan umur dalam format Tahun, Bulan, Hari secara akurat."""
        if self.tanggal_lahir:
            today = date.today()
            selisih = relativedelta(today, self.tanggal_lahir)
            total_hari = (today - self.tanggal_lahir).days
            return f"{selisih.years} Tahun, {selisih.months} Bulan, {selisih.days} Hari | ({total_hari} hari)"
            # return f"{selisih.years} Tahun, {selisih.months} Bulan, {selisih.days} Hari"
        return "Tanggal lahir tidak tersedia"

    def get_relevant_features(self):
        """Mengambil fitur terkait berdasarkan kategori pengecekan dan umur pengguna."""
        umur_hari = self.hitung_umur_hari()

        if umur_hari is not None:
            # Mengambil fitur yang sesuai dengan kategori pengecekan dan rentang umur pengguna
            fitur_tersedia = self.kategori.fitur.filter(
                min_age_in_days__lte=umur_hari,
                max_age_in_days__gte=umur_hari
            )
            return fitur_tersedia
        return []

    def __str__(self):
        return f'{self.kategori.nama_kategori} (Tanggal Lahir: {self.tanggal_lahir})'

    def save(self, *args, **kwargs):
        # Generate a new unique hash (using timestamp)
        self.content_hash = generate_unique_hash()  # Use the unique hash generator

        super().save(*args, **kwargs)
