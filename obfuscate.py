import boto3
import json

def obfuscate(json_string):
    # list_state_machines()['stateMachines'] to get the arn
    # .start_execution(arn, input='{"json": "string"}') to run the state machine
    json_dict = json.loads(json_string)
    
    arn = None
    client = boto3.client("stepfunctions")
    response = client.list_state_machines()['stateMachines']
    for state_machine in response:
        if state_machine["name"] == "state-machine-for-lambda":
            arn = state_machine["stateMachineArn"]

    print(arn)

    response = client.start_execution(stateMachineArn=arn)

    print(response)
    
    
    return {"result": "success"}
