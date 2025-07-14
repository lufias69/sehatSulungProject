# forms.py
from django import forms
from fitur_app.models import CheckupGroup, CheckupCategory


# forms.py
from django import forms
from fitur_app.models import CheckupGroup, CheckupCategory

# forms.py
from django import forms
from fitur_app.models import CheckupGroup, CheckupCategory


class CheckupGroupForm(forms.ModelForm):
    class Meta:
        model = CheckupGroup
        fields = ['nik', 'nama',  'tanggal_lahir', 'jenis_kelamin', 'nama_ibu', 'nik_ibu', 'foto', 'desa']

    def __init__(self, *args, **kwargs):
        kategori = kwargs.pop('kategori', None)  # Mendapatkan kategori dari view
        super(CheckupGroupForm, self).__init__(*args, **kwargs)

        # Menambahkan kategori yang dipilih pada form
        if kategori:
            self.fields['kategori'] = forms.ModelChoiceField(queryset=CheckupCategory.objects.filter(id=kategori.id),
                                                             initial=kategori,
                                                             widget=forms.HiddenInput())  # Menyembunyikan kategori dan set nilai otomatis
            # Pastikan kategori tidak diwajibkan untuk diisi karena sudah di-set otomatis
            self.fields['kategori'].required = False

            # Menyesuaikan apakah Nama Ibu dan NIK Ibu harus ditampilkan

            if kategori.nama_kategori == 'Anak':
                # Jika kategori Balita, maka NIK tidak diperlukan
                self.fields['nik'].required = False
                self.fields.pop('nik', None)  # Menghapus NIK dari form jika kategori Balita
                self.fields['nama_ibu'].required = True  # Nama ibu dan NIK ibu tetap diperlukan
                self.fields['nik_ibu'].required = True
            else:
                # Jika kategori selain Balita, NIK harus diisi
                self.fields['nik'].required = True
                self.fields['nama_ibu'].required = False
                self.fields['nik_ibu'].required = False

            # Foto tidak wajib
            self.fields['foto'].required = False

    def clean(self):
        cleaned_data = super().clean()
        kategori = cleaned_data.get('kategori')
        tanggal_lahir = cleaned_data.get('tanggal_lahir')
        nik = cleaned_data.get('nik')
        nama_ibu = cleaned_data.get('nama_ibu')
        nik_ibu = cleaned_data.get('nik_ibu')

        # Validasi untuk kategori bayi
        if kategori and kategori.nama_kategori == 'Balita' and not (nama_ibu and nik_ibu):
            raise forms.ValidationError("Nama ibu dan NIK ibu harus diisi untuk bayi.")

        # Validasi untuk kategori dewasa
        if kategori and kategori.nama_kategori != 'Balita' and not nik:
            raise forms.ValidationError("NIK harus diisi untuk orang dewasa.")

        return cleaned_data


class CategorySelectionForm(forms.Form):
    kategori = forms.ModelChoiceField(queryset=CheckupCategory.objects.all(), empty_label="Pilih Kategori")
