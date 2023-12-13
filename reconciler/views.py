import pandas as pd
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
                # Read CSV files
                source_df = pd.read_csv(uploaded_file.source_file.path)
                target_df = pd.read_csv(uploaded_file.target_file.path)

                # Identify the unique column
                unique_column = source_df.columns[0]

                # Strip leading and trailing spaces from column names
                source_df.columns = source_df.columns.str.strip()
                target_df.columns = target_df.columns.str.strip()

                # Identify records present in the source but missing in the target
                missing_in_target = source_df[~source_df[unique_column].isin(target_df[unique_column])]

                # Identify records present in the target but missing in the source
                missing_in_source = target_df[~target_df[unique_column].isin(source_df[unique_column])]

                # Convert DataFrames to HTML tables for display
                missing_in_target_html = missing_in_target.to_html()
                missing_in_source_html = missing_in_source.to_html()

                return render(request, 'uploader/comparison_result.html', {
                    'missing_in_target': missing_in_target_html,
                    'missing_in_source': missing_in_source_html,
                })

            except Exception as e:
                #trace error
                print(e)
    else:
        form = FileUploadForm()
    return render(request, 'reconciler/upload_file.html', {'form': form})

def upload_success():
    return render(request, 'reconciler/upload_success.html')