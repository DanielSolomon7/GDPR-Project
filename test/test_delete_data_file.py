from src.delete_data_file import delete_data_file
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
            "people_data.csv",
            test_bucket,
            "people_data.csv",
        )
        yield s3


@pytest.fixture(scope="function")
def target_bucket():
    with mock_aws():
        s3 = boto3.client("s3")
        test_bucket = "ds-target-bucket-123"
        s3.create_bucket(
            Bucket=test_bucket,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        s3.upload_file(
            "test/obfuscated_people_data.csv",
            test_bucket,
            "obfuscated_people_data.csv",
        )
        yield s3


class TestDeleteDataFile:
    @mock_aws
    def test_function_returns_a_dict(self, storage_bucket, target_bucket):
        test_file_name = "people_data.csv"
        output = delete_data_file(test_file_name)
        assert isinstance(output, dict)

    @mock_aws
    def test_function_deletes_given_csv_file_from_storage_bucket(
        self, storage_bucket, target_bucket
    ):
        s3 = storage_bucket
        test_file_name = "people_data.csv"
        output = delete_data_file(test_file_name)
        expected = {"result": "success"}
        assert output == expected

        response = s3.list_objects(
            Bucket="ds-storage-bucket-123",
        )
        assert "Contents" not in response

    @mock_aws
    def test_function_deletes_given_csv_file_from_target_bucket(
        self, storage_bucket, target_bucket
    ):
        s3 = target_bucket
        test_file_name = "people_data.csv"
        output = delete_data_file(test_file_name)
        expected = {"result": "success"}
        assert output == expected

        response = s3.list_objects(
            Bucket="ds-target-bucket-123",
        )
        assert "Contents" not in response
