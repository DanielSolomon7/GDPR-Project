from src.obfuscate import obfuscate
import pytest
from moto import mock_aws
import boto3


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


@pytest.fixture(scope="function")
def step_function():
    with mock_aws():
        client = boto3.client("stepfunctions")
        response = client.create_state_machine(
            name="state-machine-for-lambda",
            definition="""{
  "Comment": "A description of my state machine",
  "StartAt": "Lambda Invoke",
  "States": {
    "Lambda Invoke": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Output": "{% $states.result.Payload %}",
      "Arguments": {
        "FunctionName": "arn:aws:lambda:eu-west-2:750552037637:function:lambda_func",
        "Payload": "{% $states.input %}"
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2,
          "JitterStrategy": "FULL"
        }
      ],
      "End": true
    }
  },
  "QueryLanguage": "JSONata"
}""",
            roleArn="arn:aws:iam::750552037637:role/role_for_state_machine",
        )
        yield client


class TestObfuscate:
    def test_function_returns_a_dict(
        self, storage_bucket, target_bucket, step_function
    ):
        test_json = '{"file_to_obfuscate": "people_data.csv", "pii_fields": ["name", "email_address"]}'
        output = obfuscate(test_json)
        assert isinstance(output, dict)

    def test_function_adds_obfuscated_file_to_target_bucket(
        self, storage_bucket, target_bucket, step_function
    ):
        s3 = target_bucket
        test_json = '{"file_to_obfuscate": "people_data.csv", "pii_fields": ["name", "email_address"]}'
        output = obfuscate(test_json)
        assert output == {"result": "success"}

        response = s3.list_objects(
            Bucket="ds-target-bucket-123",
        )
        assert response["Contents"][0]["Key"] == "obfuscated_people_data.csv"
