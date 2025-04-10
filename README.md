# GDPR-Obfuscator-Project
This project is a GDPR Obfuscator tool, which uses AWS cloud infrastructure.
The project uses S3 buckets to store the data, AWS Lambda to run the code, and Terraform is used to deploy the cloud infrastructure.
The tool takes data from an unobfuscated CSV file, in the 'storage' S3 bucket, and creates a new version of the file with the chosen fields obfuscated, and uploads this to the 'target' S3 bucket.

## Setup
Create virtual environment:
```bash
 make create-environment
```

In the root directory, export PYTHONPATH to the current working directory: export PYTHONPATH=$(pwd)

Install packages:
```bash
make install-requirements
```

Run checks on the Lambda Python code - unit, security, and PEP-8:
```bash
make run-checks
```

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