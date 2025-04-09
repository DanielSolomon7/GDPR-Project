import boto3


def delete_data_file(file_name):
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
