from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, LaporanKerusakan

# Form untuk pendaftaran user baru (Register)
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label="Nama Depan")
    last_name = forms.CharField(max_length=30, required=True, label="Nama Belakang")
    phone_number = forms.CharField(required=True, label="No. Telepon")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2', 'role']

# Form untuk mengajukan laporan kerusakan
class LaporanForm(forms.ModelForm):
    class Meta:
        model = LaporanKerusakan
        fields = ['alamat', 'jenis_kerusakan', 'tingkat_kerusakan', 'deskripsi', 'kota', 'image']
    
    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image and hasattr(image, 'content_type'):
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
        self.fields['kota'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].label = "Unggah Gambar Kerusakan"


# Form untuk Edit Profil (Update profil pengguna)
class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']
