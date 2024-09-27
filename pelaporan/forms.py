from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, LaporanKerusakan

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2', 'role']

# Form untuk mengajukan laporan kerusakan
class LaporanForm(forms.ModelForm):
    class Meta:
        model = LaporanKerusakan
        fields = ['alamat', 'jenis_kerusakan', 'tingkat_kerusakan', 'deskripsi','provinsi','image']

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 4 * 1024 * 1024:
                raise forms.ValidationError("Ukuran file terlalu besar (maksimal 4MB).")
            if not image.content_type in ["image/jpeg", "image/png"]:
                raise forms.ValidationError("Format file tidak didukung. Gunakan JPEG atau PNG.")
        return image

    def __init__(self, *args, **kwargs):
        super(LaporanForm, self).__init__(*args, **kwargs)
        self.fields['alamat'].label = "Alamat Rumah Dinas"
        self.fields['jenis_kerusakan'].label = "Jenis Kerusakan"
        self.fields['tingkat_kerusakan'].label = "Tingkat Kerusakan"
        self.fields['deskripsi'].label = "Deskripsi Kerusakan"
        self.fields['provinsi'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].label = "Unggah Gambar Kerusakan"

class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Tanggal Mulai',
        required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Tanggal Akhir',
        required=False
    )