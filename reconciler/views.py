import pandas as pd
from django.shortcuts import render, redirect
from pandas.testing import assert_frame_equal

from reconciler.forms import FileUploadForm

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                uploaded_file = form.save()

                # Read CSV files
                source_df = pd.read_csv(uploaded_file.source_file.path)
                target_df = pd.read_csv(uploaded_file.target_file.path)

                # Strip leading and trailing spaces from column names
                source_df.columns = source_df.columns.str.strip()
                target_df.columns = target_df.columns.str.strip()

                # Identify records present in the source but missing in the target
                missing_in_target = source_df[~source_df.isin(target_df.to_dict(orient='list')).all(axis=1)]

                # Identify records present in the target but missing in the source
                missing_in_source = target_df[~target_df.isin(source_df.to_dict(orient='list')).all(axis=1)]

                # Identify records with field discrepancies
                df_dff = source_df.compare(target_df)
                field_discrepancies = df_dff[df_dff.ne(0).any(axis=1)]

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
