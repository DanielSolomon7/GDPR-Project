import boto3


def upload_data_file(file_name):
    try:
        s3 = boto3.client("s3")

        s3.upload_file(
            file_name,
            "ds-storage-bucket-123",
            file_name,
        )
        return {"result": "success"}

    except FileNotFoundError as e:
        raise FileNotFoundError("Given file does not exist.")
    except Exception as e:
        raise (e)
