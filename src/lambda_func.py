import boto3
import pandas as pd
from io import BytesIO, StringIO


def lambda_handler(event, context):
    """Takes the name of a file, and uploads the file in the
    S3 storage bucket

    Paramaters:
        event (dict): a dict of the json entered into the Lambda.
                      should contains the following keys:
                      'file_to_obfuscate' (str): the name of the CSV
                                                 file to obfuscate
                      'pii_fields' (list): a list of strings of the
                                           columns to obfuscate

    Returns:
        dict: a dict with a key of 'result', and a value of 'success',
        saying that the file was obfuscated and uploaded to the target
        bucket
    """
    if not isinstance(event, dict):
        raise TypeError("Invalid event input - not a JSON.")
    if not isinstance(event["pii_fields"], list):
        raise TypeError("pii_fields must be a list of valid column names.")
    if len(event["pii_fields"]) == 0:
        raise ValueError("No column names given in pii_fields list.")
    if list(event.keys()) != ["file_to_obfuscate", "pii_fields"] and list(
        event.keys()
    ) != ["pii_fields", "file_to_obfuscate"]:
        raise ValueError(
            "Invalid keys given in JSON - there must "
            "be only two keys: 'file_to_obfuscate' and 'pii_fields'."
        )

    try:
        s3 = boto3.client("s3")
        file_name = event["file_to_obfuscate"]
        obfuscated_file_name = f"obfuscated_{file_name}"

        """Get CSV file from the storage bucket"""
        response = s3.get_object(Bucket="ds-storage-bucket-123", Key=file_name)

        """Convert the CSV File to a DataFrame"""
        content = response["Body"].read()
        df = pd.read_csv(BytesIO(content))

        """Obfuscate given columns"""
        for i, row in df.iterrows():
            for column_name in event["pii_fields"]:
                if column_name in list(df.columns):
                    df.at[i, column_name] = "***"
                else:
                    raise ValueError("Invalid column name given: "
                                     f"{column_name}")

        """Create new CSV file from DataFrame"""
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, header=True, index=False)

        """Upload new CSV file to the target bucket"""
        s3.put_object(
            Bucket="ds-target-bucket-123",
            Body=csv_buffer.getvalue(),
            Key=obfuscated_file_name,
        )

        return {
            "result": f"File {obfuscated_file_name} has been "
            "created and uploaded to the target bucket."
        }

    except Exception as e:
        raise (e)
