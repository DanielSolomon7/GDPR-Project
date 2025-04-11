import boto3


def delete_data_file(file_name):
    """Takes the name of a file, and deletes both the file in the
    S3 storage bucket, and the obfuscated file in the S3
    target bucket

    Paramaters:
        file_name (str): the name of the file to delete

    Returns:
        dict: a dict with a key of 'result', and a value of 'success'
    """
    if not isinstance(file_name, str):
        raise TypeError("Given file name must be a string")

    try:
        s3 = boto3.client("s3")

        s3.delete_object(
            Bucket="ds-storage-bucket-123",
            Key=file_name,
        )

        s3.delete_object(
            Bucket="ds-target-bucket-123",
            Key=f"obfuscated_{file_name}",
        )

        return {"result": "success"}

    except Exception as e:
        raise (e)
