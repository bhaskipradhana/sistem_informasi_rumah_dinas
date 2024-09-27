from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, LaporanForm, UserProfileForm
from .models import LaporanKerusakan
from django.contrib import messages
from django import forms
from django.shortcuts import render
from .models import LaporanKerusakan
from django.utils import timezone

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'pelaporan/register.html', {'form': form})

def home(request):
    return render(request, 'pelaporan/home.html')

@login_required
def profile(request):
    return render(request, 'pelaporan/profile.html')

@login_required
def create_laporan(request):
    if request.user.role != 'requester':
        messages.error(request, 'Anda tidak memiliki akses.')
        return redirect('home')
    if request.method == 'POST':
        form = LaporanForm(request.POST,request.FILES)
        if form.is_valid():
            laporan = form.save(commit=False)
            laporan.requester = request.user
            laporan.save()
            messages.success(request, 'Laporan berhasil dikirim.')
            return redirect('list_laporan')
    else:
        form = LaporanForm()
    return render(request, 'pelaporan/create_laporan.html', {'form': form})


@login_required
def update_laporan(request, pk):
    laporan = get_object_or_404(LaporanKerusakan, pk=pk, requester=request.user)
    
    if laporan.status != 'review':
        messages.error(request, 'Laporan tidak dapat diubah karena statusnya bukan "Sedang di review".')
        return redirect('list_laporan')
    
    if request.method == 'POST':
        form = LaporanForm(request.POST, request.FILES, instance=laporan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Laporan berhasil diperbarui.')
            return redirect('list_laporan')
    else:
        form = LaporanForm(instance=laporan)
    
    return render(request, 'pelaporan/update_laporan.html', {'form': form, 'laporan': laporan})


@login_required
def delete_laporan(request, pk):
    laporan = get_object_or_404(LaporanKerusakan, pk=pk, requester=request.user)

    if laporan.status != 'review':
        messages.error(request, 'Laporan tidak dapat dihapus karena statusnya bukan "Sedang di review".')
        return redirect('list_laporan')

    if request.method == 'POST':
        laporan.delete()
        messages.success(request, 'Laporan berhasil dihapus.')
        return redirect('list_laporan')

    return render(request, 'pelaporan/delete_laporan.html', {'laporan': laporan})


@login_required
def list_laporan(request):
    if request.user.role == 'requester':
        laporan_list = LaporanKerusakan.objects.filter(requester=request.user)
    elif request.user.role == 'approver':
        # Ambil semua laporan tanpa filter status
        laporan_list = LaporanKerusakan.objects.all()
    else:
        laporan_list = LaporanKerusakan.objects.none()
    return render(request, 'pelaporan/list_laporan.html', {'laporan_list': laporan_list})

@login_required
def approve_laporan(request, pk):
    if request.user.role != 'approver':
        messages.error(request, 'Anda tidak memiliki akses.')
        return redirect('home')
    laporan = get_object_or_404(LaporanKerusakan, pk=pk)
    if request.method == 'POST':
        tanggal_pengerjaan = request.POST.get('tanggal_pengerjaan')
        if tanggal_pengerjaan:
            laporan.status = 'approved'
            laporan.tanggal_pengerjaan = tanggal_pengerjaan
            laporan.save()
            messages.success(request, 'Laporan telah di-approve.')
            return redirect('list_laporan')
    return render(request, 'pelaporan/approve_laporan.html', {'laporan': laporan})


@login_required
def view_laporan(request, pk):
    laporan = get_object_or_404(LaporanKerusakan, pk=pk)
    return render(request, 'pelaporan/view_laporan.html', {'laporan': laporan})


@login_required
def reject_laporan(request, pk):
    if request.user.role != 'approver':
        messages.error(request, 'Anda tidak memiliki akses.')
        return redirect('home')
    laporan = get_object_or_404(LaporanKerusakan, pk=pk)
    if request.method == 'POST':
        notes = request.POST.get('notes')
        laporan.status = 'rejected'
        laporan.notes = notes
        laporan.save()
        messages.success(request, 'Laporan telah di-reject.')
        return redirect('list_laporan')
    return render(request, 'pelaporan/reject_laporan.html', {'laporan': laporan})


@login_required
def list_laporan(request):
    if request.user.role == 'requester':
        laporan_list = LaporanKerusakan.objects.filter(requester=request.user)
    elif request.user.role == 'approver':
        status_filter = request.GET.get('status', '')
        if status_filter:
            laporan_list = LaporanKerusakan.objects.filter(status=status_filter)
        else:
            laporan_list = LaporanKerusakan.objects.all()
    else:
        laporan_list = LaporanKerusakan.objects.none()
    return render(request, 'pelaporan/list_laporan.html', {'laporan_list': laporan_list})

@login_required
def view_laporan(request, pk):
    laporan = get_object_or_404(LaporanKerusakan, pk=pk)
    return render(request, 'pelaporan/view_laporan.html', {'laporan': laporan})


class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

@login_required
def jadwal_perbaikan(request):
    if request.user.role != 'approver':
        return redirect('home')  # Atau tampilkan pesan error

    form = DateRangeForm(request.GET or None)
    laporan_list = LaporanKerusakan.objects.filter(status='approved')

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')

        if start_date and end_date:
            laporan_list = laporan_list.filter(
                tanggal_pengerjaan__range=[start_date, end_date]
            )
        elif start_date:
            laporan_list = laporan_list.filter(
                tanggal_pengerjaan__gte=start_date
            )
        elif end_date:
            laporan_list = laporan_list.filter(
                tanggal_pengerjaan__lte=end_date
            )
    else:
        form = DateRangeForm()

    return render(request, 'pelaporan/jadwal_perbaikan.html', {'form': form, 'laporan_list': laporan_list})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('profile')  # Redirect ke halaman profil setelah update
    else:
        user_form = UserProfileForm(instance=request.user)

    return render(request, 'pelaporan/edit_profile.html', {
        'user_form': user_form
    })