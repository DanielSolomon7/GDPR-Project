# GDPR-Project

## Setup
Create virtual environment: python -m venv venv

Activate virtual environment: source venv/bin/activate

In the root directory, export PYTHONPATH to the current working directory: export PYTHONPATH=$(pwd)

Install packages: pip install -r requirements.txt

Run unit tests on the Python code: pytest test -vvvrP

Run security tests on the Python code: bandit src/lambda_func.py src/upload_data_file.py src/run_upload_data_file.py src/delete_data_file.py src/run_delete_data_file.py test/test_lambda_func.py test/test_upload_data_file.py test/test_delete_data_file.py

Run PEP-8 tests on the code: flake8 src test

## Deployment
Go into terraform file: cd terraform

Set up the Terraform files: terraform init

Plan the Terraform deployment: terraform plan

Apply the Terraform infrastructure: terraform apply

Go back into the root directory

Make sure the CSV data file is in the root directory.

In the root directory, upload the CSV data file: python src/run_upload_data_file.py - then enter the name of the file - make sure it is the correct name, otherwise an error will occur. If no error occurs, the file has been uploaded.

Log into AWS, and run the 'state-machine-for-lambda' state machine, entering a JSON string with a 'file_to_obfuscate' key and a value of a string of the file name, and a 'pii_fields' key, with a value of a list of strings of column names of the desired columns to obfuscate. For example:
{
    "file_to_obfuscate": "people_data.csv",
    "pii_fields": ["name", "email_address"]
}

Once run, an obfuscated file of the file that was entered, with the chosen columns obfuscated, should be uploaded into the target bucket.

## Deleting
Before running terraform destroy, delete files from the storage and target buckets. Run function in root directory: python src/run_delete_data_file.py - then enter the name of the file - make sure it is the correct name.

To delete the cloud infrastrcuture, cd into the terraform folder and run: terraform destroy.