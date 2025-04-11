from src.upload_data_file import upload_data_file
import pytest
import boto3
from moto import mock_aws


@pytest.fixture(scope="function")
def empty_storage_bucket():
    with mock_aws():
        s3 = boto3.client("s3")
        test_bucket = "ds-storage-bucket-123"
        s3.create_bucket(
            Bucket=test_bucket,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        yield s3


class TestUploadDataFile:
    @mock_aws
    def test_function_returns_a_dict(self, empty_storage_bucket):
        test_file_name = "people_data.csv"
        output = upload_data_file(test_file_name)
        assert isinstance(output, dict)

    @mock_aws
    def test_function_uploads_local_csv_file_to_storage_bucket(
        self, empty_storage_bucket
    ):
        s3 = empty_storage_bucket
        test_file_name = "people_data.csv"
        output = upload_data_file(test_file_name)
        expected = {"result": "success"}
        assert output == expected

        response = s3.list_objects(
            Bucket="ds-storage-bucket-123",
        )

        assert response["Contents"][0]["Key"] == test_file_name

    @mock_aws
    def test_function_handles_file_name_of_non_existent_file(
        self, empty_storage_bucket
    ):
        test_file_name = "hi.csv"

        with pytest.raises(Exception) as e:
            upload_data_file(test_file_name)
        assert str(e.value) == "Given file does not exist."

    def test_function_handles_non_csv_file_given(
        self, empty_storage_bucket
    ):
        test_file_name = "people_data.json"

        with pytest.raises(Exception) as e:
            upload_data_file(test_file_name)
        assert str(e.value) == "Given file must be CSV."
