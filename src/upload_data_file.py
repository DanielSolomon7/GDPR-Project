import boto3


def upload_data_file(file_name):
    """Takes the name of a file, and uploads the file in the
    S3 storage bucket

    Paramaters:
        file_name (str): the name of the file to upload

    Returns:
        dict: a dict with a key of 'result', and a value of 'success',
        if the upload was successful
    """
    if file_name[-4:] != ".csv":
        raise ValueError("Given file must be CSV.")

    try:
        s3 = boto3.client("s3")

        s3.upload_file(
            file_name,
            "ds-storage-bucket-123",
            file_name,
        )
        return {"result": "success"}

    except FileNotFoundError:
        raise FileNotFoundError("Given file does not exist.")
    except Exception as e:
        raise (e)
