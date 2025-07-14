# alamat_app/forms.py
from django import forms
from .models import Provinsi, KabupatenKota, Kecamatan, Desa

class AlamatForm(forms.Form):
    provinsi = forms.ModelChoiceField(queryset=Provinsi.objects.all(), label="Provinsi")
    kabupaten_kota = forms.ModelChoiceField(queryset=KabupatenKota.objects.none(), label="Kabupaten/Kota")
    kecamatan = forms.ModelChoiceField(queryset=Kecamatan.objects.none(), label="Kecamatan")
    desa = forms.ModelChoiceField(queryset=Desa.objects.none(), label="Desa")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'provinsi' in self.data:
            self.fields['kabupaten_kota'].queryset = KabupatenKota.objects.filter(provinsi=self.data.get('provinsi'))
            if 'kabupaten_kota' in self.data:
                self.fields['kecamatan'].queryset = Kecamatan.objects.filter(kabupaten_kota=self.data.get('kabupaten_kota'))
                if 'kecamatan' in self.data:
                    self.fields['desa'].queryset = Desa.objects.filter(kecamatan=self.data.get('kecamatan'))


# alamat_app/forms.py
from django import forms
from .models import Provinsi, KabupatenKota, Kecamatan, Desa

class ProvinsiForm(forms.ModelForm):
    class Meta:
        model = Provinsi
        fields = ['nama']


class KabupatenKotaForm(forms.ModelForm):
    class Meta:
        model = KabupatenKota
        fields = ['provinsi', 'nama']


class KecamatanForm(forms.ModelForm):
    class Meta:
        model = Kecamatan
        fields = ['kabupaten_kota', 'nama']


class DesaForm(forms.ModelForm):
    class Meta:
        model = Desa
        fields = ['kecamatan', 'nama']
from django import forms
from .models import KabupatenKota

class KabupatenForm(forms.ModelForm):
    class Meta:
        model = KabupatenKota
        fields = ['nama']  # Sesuaikan dengan field yang Anda inginkan

class KecamatanForm(forms.ModelForm):
    class Meta:
        model = Kecamatan
        fields = ['nama']  # Sesuaikan dengan field yang Anda inginkan

class DesaForm(forms.ModelForm):
    class Meta:
        model = Desa
        fields = ['nama']  # Sesuaikan dengan field yang Anda inginkan


from django import forms
from .models import Desa

class DesaSearchForm(forms.Form):
    search = forms.CharField(max_length=255, required=False, label="Nama Desa")
