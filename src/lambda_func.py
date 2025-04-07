import boto3

def lambda_handler():
    s3 = boto3.client("s3")
