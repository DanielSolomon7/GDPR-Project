import boto3
import json

def obfuscate(json_string):
    # list_state_machines()['stateMachines'] to get the arn
    # .start_execution(arn, input='{"json": "string"}') to run the state machine
    json_dict = json.loads(json_string)
    
    """Get the arn of the state machine"""
    arn = None
    client = boto3.client("stepfunctions")
    response = client.list_state_machines()['stateMachines']
    for state_machine in response:
        if state_machine["name"] == "state-machine-for-lambda":
            arn = state_machine["stateMachineArn"]

    """Execute the state machine"""
    response = client.start_execution(stateMachineArn=arn)

    print(response)

    file_name = json_dict["file_to_obfuscate"]

    """Download the Obfuscated file"""
    s3 = boto3.client("s3")
    s3.download_file("ds-target-bucket-123",
                     f"obfuscated_{file_name}",
                     f"obfuscated_{file_name}")
    
    
    return {"result": "success"}

obfuscate('''{
            "file_to_obfuscate": "people_data.csv",
            "pii_fields": ["name", "email_address"]
        }''')
