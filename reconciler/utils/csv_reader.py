import pandas as pd


def read_source_file(file_path):
    # Read the src file using Pandas
    df = pd.read_csv(file_path)
    return df

def read_target_file(file_path):
    # read the target file using pandas
    df = pd.read_csv(file_path)
    return df