from src.upload_data_file import upload_data_file
import pytest
import boto3
from moto import mock_aws


@pytest.fixture(scope="function")
def storage_bucket():
    with mock_aws():
        s3 = boto3.client("s3")
        test_bucket = "ds-storage-bucket-123"
        s3.create_bucket(
            Bucket=test_bucket,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        s3.upload_file(
            "test/people_data.csv",
            test_bucket,
            "people_data.csv",
        )
        yield s3


class TestUploadDataFile:
    @mock_aws
    def test_function_returns_a_dict(self):
        input = "test/people_data.csv"
        output = upload_data_file(input)
        assert isinstance(output, dict)
