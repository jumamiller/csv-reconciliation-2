# reconciler_utils.py
import pandas as pd


def reconcile_uploaded_files(source_path, target_path):
    try:
        # Read CSV files
        source_df = pd.read_csv(source_path)
        target_df = pd.read_csv(target_path)

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

        return missing_in_target, missing_in_source, field_discrepancies

    except Exception as e:
        # Trace error
        print(e)
        return None, None, None
