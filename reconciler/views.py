import pandas as pd
from django.shortcuts import render

from reconciler.forms import FileUploadForm
from reconciler.utils.csv_reader import reconcile_uploaded_files


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                uploaded_file = form.save()

                # Call the utility function
                source_path = uploaded_file.source_file.path
                target_path = uploaded_file.target_file.path
                missing_in_target, missing_in_source, field_discrepancies = reconcile_uploaded_files(source_path,
                                                                                                     target_path)
                # Convert DataFrames to HTML tables for display
                missing_in_target_html = missing_in_target.to_html()
                missing_in_source_html = missing_in_source.to_html()
                field_discrepancies_html = field_discrepancies.to_html()

                return render(request, 'uploader/comparison_result.html', {
                    'missing_in_target': missing_in_target_html,
                    'missing_in_source': missing_in_source_html,
                    'field_discrepancies': field_discrepancies_html,
                })

            except Exception as e:
                # Trace error
                print(e)
    else:
        form = FileUploadForm()

    return render(request, 'reconciler/upload_file.html', {'form': form})
