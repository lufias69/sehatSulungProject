# fitur_app/forms.py

from django import forms

from alamat_app.models import Provinsi
from .models import Feature



class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['kategori','name', 'description', 'image', 'min_age_in_days', 'max_age_in_days', 'initial_instructions', 'final_instructions', 'requires_analysis']  # Added new fields

    # Optionally, you can add custom validation or widgets for these fields if needed
    min_age_in_days = forms.IntegerField(required=False, label="Minimum Age (in days)", help_text="Enter the minimum age in days")
    max_age_in_days = forms.IntegerField(required=False, label="Maximum Age (in days)", help_text="Enter the maximum age in days")

    requires_analysis = forms.BooleanField(
        required=False,  # This field is optional, default is False
        label="Requires Analysis",
        help_text="Check this if the feature requires analysis"
    )

from django import forms
from .models import CheckupGroup, CheckupCategory


# forms.py
from django import forms
from .models import CheckupGroup, CheckupCategory

class CheckupGroupForm(forms.ModelForm):
    # provinsi = forms.ModelChoiceField(queryset=Provinsi.objects.all(), required=False)


    class Meta:
        model = CheckupGroup
        fields = ['nik', 'nama', 'tanggal_lahir', 'jenis_kelamin', 'nama_ibu', 'nik_ibu', 'foto', 'desa']
        widgets = {
            'jenis_kelamin': forms.Select(choices=CheckupGroup.JENIS_KELAMIN_CHOICES),
            'tanggal_lahir': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        kategori = kwargs.pop('kategori', None)  # Mendapatkan kategori dari view
        super(CheckupGroupForm, self).__init__(*args, **kwargs)

        # Jika kategori ada, atur validasi dan tampilan field berdasarkan kategori
        if kategori:
            self.fields['kategori'] = forms.ModelChoiceField(queryset=CheckupCategory.objects.filter(id=kategori.id),
                                                             initial=kategori,
                                                             widget=forms.HiddenInput())  # Menyembunyikan kategori jika tidak perlu diedit


            # Menyesuaikan apakah Nama Ibu dan NIK Ibu harus ditampilkan
            if kategori.nama_kategori == 'Anak':
                # Jika kategori Balita, maka NIK tidak diperlukan
                self.fields['nik'].required = False
                self.fields.pop('nik', None)  # Menghapus field NIK dari form

                self.fields['nama_ibu'].required = True  # Nama ibu dan NIK ibu tetap diperlukan
                self.fields['nik_ibu'].required = True
            else:
                # Jika kategori selain Balita, NIK harus diisi
                self.fields['nik'].required = True
                self.fields['nama_ibu'].required = False
                self.fields['nik_ibu'].required = False

            # Membuat foto tidak wajib
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


class CheckupCategoryForm(forms.ModelForm):
    class Meta:
        model = CheckupCategory
        fields = ['nama_kategori']
