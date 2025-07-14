from django.shortcuts import render, redirect
from .models import MediaItem
from .forms import MediaItemForm

def media_list(request):
    items = MediaItem.objects.order_by('-uploaded_at')  # Menampilkan terbaru di atas
    return render(request, 'media_center_app/media_list.html', {
        'items': items,
    })

def media_upload(request):
    if request.method == 'POST':
        form = MediaItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('media_center_app:media_list')
    else:
        form = MediaItemForm()
    return render(request, 'media_center_app/media_upload.html', {
        'form': form
    })
