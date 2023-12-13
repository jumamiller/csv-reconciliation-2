from django.http import request
from django.shortcuts import render, redirect

from reconciler.forms import FileUploadForm
from .utils.csv_reader import read_source_file, read_target_file

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                uploaded_file = form.save()
                # src file_path
                source_file_path = uploaded_file.source_file.path
                df_source = read_source_file(source_file_path)
                # target file_path
                target_file_path = uploaded_file.target_file.path
                df_target = read_target_file(target_file_path)
                mismatched_columns = set(df_source.columns) ^ set(df_target.columns)
                # save the result to a new csv file
                if not mismatched_columns:
                    print("The source file has the same columns as the target file.")
                else:
                    print("Mismatched columns:")
                    print(mismatched_columns)
                return redirect('upload_success')
            except Exception as e:
                print(e)
    else:
        form = FileUploadForm()
    return render(request, 'reconciler/upload_file.html', {'form': form})

def upload_success():
    return render(request, 'reconciler/upload_success.html')