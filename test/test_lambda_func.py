from src.lambda_func import lambda_handler
import boto3
from moto import mock_aws
import pytest
import pandas as pd
from io import BytesIO


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
        yield s3


class TestLambdaFunc:
    @mock_aws
    def test_function_returns_a_dict(
        self, storage_bucket, target_bucket
    ):
        input = {
            "file_to_obfuscate": "people_data.csv",
            "pii_fields": ["name", "email_address"]
        }
        output = lambda_handler(input, "")
        assert isinstance(output, dict)

    @mock_aws
    def test_function_creates_csv_file_with_obfuscated_data(
        self, storage_bucket, target_bucket
    ):
        s3 = target_bucket
        input = {
            "file_to_obfuscate": "people_data.csv",
            "pii_fields": ["name", "email_address"]
        }
        output = lambda_handler(input, "")
        assert output == {
            "result": "File obfuscated_people_data.csv "
            "has been created and uploaded to "
            "the target bucket."
        }

        response = s3.get_object(
            Bucket="ds-target-bucket-123", Key="obfuscated_people_data.csv"
        )
        content = response["Body"].read()
        df = pd.read_csv(BytesIO(content))

        assert list(df.columns) == [
            "student_id",
            "name",
            "course",
            "graduation_date",
            "email_address",
        ]
        assert list(df.iloc[0]) == [1, "***", "Software", "2024-03-31", "***"]
        assert list(df.iloc[8]) == [9, "***", "Data", "2024-06-30", "***"]

    @mock_aws
    def test_function_handles_non_existent_file_name(
        self, storage_bucket, target_bucket
    ):
        input = {"file_to_obfuscate": "hi.csv",
                 "pii_fields": ["name", "email_address"]}
        with pytest.raises(Exception) as e:
            lambda_handler(input, "")
        assert str(e.value) == "Given file not found."

    @mock_aws
    def test_function_handles_invalid_type_for_file_name(
        self, storage_bucket, target_bucket
    ):
        input = {"file_to_obfuscate": 5,
                 "pii_fields": ["name", "email_address"]}
        with pytest.raises(Exception) as e:
            lambda_handler(input, "")
        assert str(e.value) == ("Invalid 'file_to_obfuscate' input "
                                "- not a string.")

    @mock_aws
    def test_function_handles_invalid_column_name(
        self, storage_bucket, target_bucket
    ):
        input = {"file_to_obfuscate": "people_data.csv",
                 "pii_fields": ["name", 5]}
        with pytest.raises(Exception) as e:
            lambda_handler(input, "")
        assert str(e.value) == "Invalid column name given: 5"

    @mock_aws
    def test_function_handles_non_list_given_for_column_names(
        self, storage_bucket, target_bucket
    ):
        input = {"file_to_obfuscate": "people_data.csv",
                 "pii_fields": "name"}
        with pytest.raises(Exception) as e:
            lambda_handler(input, "")
        assert str(e.value) == ("pii_fields must be a "
                                "list of valid column names.")

    @mock_aws
    def test_function_handles_empty_list_given_for_column_names(
        self, storage_bucket, target_bucket
    ):
        input = {"file_to_obfuscate": "people_data.csv",
                 "pii_fields": []}
        with pytest.raises(Exception) as e:
            lambda_handler(input, "")
        assert str(e.value) == "No column names given in pii_fields list."

    @mock_aws
    def test_function_handles_invalid_key_given(
        self, storage_bucket, target_bucket
    ):
        input = {"hello": "people_data.csv",
                 "pii_fields": ["name", "email_address"]}
        with pytest.raises(Exception) as e:
            lambda_handler(input, "")
        assert (
            str(e.value)
            == "Invalid keys given in JSON - there must be "
            "only two keys: 'file_to_obfuscate' and 'pii_fields'."
        )

    @mock_aws
    def test_function_handles_non_json_given(
        self, storage_bucket, target_bucket
    ):
        input = 5
        with pytest.raises(Exception) as e:
            lambda_handler(input, "")
        assert str(e.value) == "Invalid event input - not a JSON."

    @mock_aws
    def test_function_handles_non_csv_file_given(
        self, storage_bucket, target_bucket
    ):
        input = {"file_to_obfuscate": "people_data.json",
                 "pii_fields": ["name", "email_address"]}
        with pytest.raises(Exception) as e:
            lambda_handler(input, "")
        assert str(e.value) == "Given file must be CSV."
