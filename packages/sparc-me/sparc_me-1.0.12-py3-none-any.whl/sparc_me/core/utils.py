import os
import shutil
import pandas as pd
from datetime import datetime, timezone

def add_data(source_path, destination_path, copy=True, overwrite=False):
    """Copy or move data from source folder to destination folder

    :param source_path: path to the original data
    :type source_path: string
    :param destination_path: folder path to be copied into
    :type destination_path: string
    :param copy: if True, source directory data will not be deleted after copying, defaults to True
    :type copy: bool, optional
    :param overwrite: if True, any data in the destination folder will be overwritten, defaults to False
    :type overwrite: bool, optional
    :raises FileExistsError: if the destination folder contains data and overwritten is set to False, this wil be raised.
    """

    # If overwrite is True, remove existing sample
    if os.path.exists(destination_path):
        if overwrite: 
            shutil.rmtree(destination_path)
        else:
            raise FileExistsError("Destination file already exist. Indicate overwrite argument as 'True' to overwrite the existing")

    # Create destination folder
    os.makedirs(destination_path)

    for fname in os.listdir(source_path):
        file_path = os.path.join(source_path, fname)
        if os.path.isdir(file_path):
            # Warn user if a subdirectory exist in the input_path
            print(f"Warning: Input directory consist of subdirectory {source_path}. It will be avoided during copying") 
        else:
            if copy:
                # Copy data
                shutil.copy2(file_path, destination_path)
            else:
                # Move data
                shutil.move(file_path, os.path.join(destination_path, fname))
            # Modify the manifest file
            modify_manifest(fname, destination_path)


def modify_manifest(fname, destination_path):
    # Check if manifest exist
    # If can be "xlsx", "csv" or "json"
    files = os.listdir(destination_path)
    manifest_file_path = [f for f in files if "manifest" in f]
    # Case 1: manifest file exists
    if len(manifest_file_path)!=0:
        manifest_file_path = os.path.join(destination_path, manifest_file_path[0])
        # Check the extension and read file accordingly
        extension = os.path.splitext(manifest_file_path)[-1].lower()
        if extension == ".xlsx":
            df = pd.read_excel(manifest_file_path, index_col=0)
        elif extension == ".csv":
            df = pd.read_csv(manifest_file_path)
        elif extension == ".json":
            # TODO: Check what structure a manifest json is in
            # Below code assumes json structure is like
            # '{"row 1":{"col 1":"a","col 2":"b"},"row 2":{"col 1":"c","col 2":"d"}}'
            df = pd.read_json(manifest_file_path, orient="index")
        else:
            raise ValueError(f"Unauthorized manifest file extension: {extension}")
    # Case 2: create manifest file
    else:
        # Default extension to xlsx
        extension = ".xlsx"
        # Creat manifest file path
        manifest_file_path = os.path.join(destination_path, "manifest.xlsx")
        df = pd.DataFrame(columns = ['filename', 'description', 'timestamp', 'file type'])

    # Edit manifest
    sample = destination_path.split(os.path.sep)[-1]
    subject = destination_path.split(os.path.sep)[-2]

    row = {
        'filename': os.path.splitext(fname)[0],
        'timestamp': datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        'description': f"File of subject {subject} sample {sample}",
        'file type': os.path.splitext(fname)[-1].lower()[1:]
    }
    row_pd = pd.DataFrame([row])
    df = pd.concat([df, row_pd], axis=0, ignore_index=True)
    
    # Save editted manifest file
    if extension == ".xlsx":
        df.to_excel(manifest_file_path)
    elif extension == ".csv":
        df = pd.to_csv(manifest_file_path)
    elif extension == ".json":
        df = pd.read_json(manifest_file_path, orient="index")
    return


def check_row_exist(dataframe, unique_column, unique_value):
    """Check if a row exist with given unique value

    :param dataframe: metadata dataframe that must be checked
    :type dataframe: Pandas DataFrame
    :param unique_value: value that can be used to uniquely identifies a row
    :type unique_value: string
    :return: row index of the row identified with the unique value, or -1 if there is no row corresponding to the unique value
    :rtype: int
    :raises ValueError: if more than one row can be identified with given unique value
    """
    row_index = dataframe.index[dataframe[unique_column]==unique_value].tolist()
    if not row_index:
        row_index = -1
    elif len(row_index)>1:
        error_msg = "More than one row can be identified with given unique value"
        raise ValueError(error_msg)
    else:
        row_index = row_index[0]
    return row_index
