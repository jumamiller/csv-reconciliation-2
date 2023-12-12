from django.http import request
from django.shortcuts import render, redirect

from reconciler.forms import FileUploadForm

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_success')
    else:
        form = FileUploadForm()
    return render(request, 'reconciler/upload_file.html', {'form': form})

def upload_success():
    return render(request, 'reconciler/upload_success.html')