import boto3
import pandas as pd
from io import BytesIO, StringIO


def lambda_handler(event, context):
    if not isinstance(event["pii_fields"], list):
        raise TypeError("pii_fields must be a list of valid column names.")
    if len(event["pii_fields"]) == 0:
        raise ValueError("No column names given in pii_fields list.")
    try:
        s3 = boto3.client("s3")
        file_name = event["file_to_obfuscate"]
        obfuscated_file_name =  f"obfuscated_{file_name}"

        """Get CSV file from the storage bucket"""
        response = s3.get_object(
                Bucket="ds-storage-bucket-123", Key=file_name
            )
        
        """Convert the CSV File to a DataFrame"""
        content = response["Body"].read()
        df = pd.read_csv(BytesIO(content))

        """Obfuscate given columns"""
        for i, row in df.iterrows():
            for column_name in event["pii_fields"]:
                if column_name in list(df.columns):
                    df.at[i, column_name] = '***'
                else:
                    raise ValueError(f"Invalid column name given: {column_name}")

        """Create new CSV file from DataFrame"""
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, header=True, index=False)

        """Upload new CSV file to the target bucket"""
        s3.put_object(Bucket="ds-target-bucket-123", Body=csv_buffer.getvalue(), Key=obfuscated_file_name)

        return {
            "result": f"File {obfuscated_file_name} has been created and uploaded to the target bucket."
        }
    
    except Exception as e:
        raise(e)
