# GDPR-Obfuscator-Project
This project is a GDPR Obfuscator tool, which uses AWS cloud infrastructure.
The project uses S3 buckets to store the data, AWS Lambda to run the code, a State Machine to invoke the tool, and Terraform is used to deploy the cloud infrastructure.
The tool takes data from an unobfuscated CSV file, in the 'storage' S3 bucket, and creates a new version of the file with the chosen fields obfuscated, and uploads this to the 'target' S3 bucket.

## Table of Contents
- [Installation](#installation)
- [Setup](#setup)
- [Cloud Infrastructure Deployment](#cloud-infrastructure-deployment)
- [Uploading Unobfuscated CSV File to Storage S3 Bucket](#uploading-unobfuscated-csv-file-to-storage-s3-bucket)
- [Running the Obfuscation Tool and Creating an Obfuscated File](#running-the-obfuscation-tool-and-creating-an-obfuscated-file)
- [Deleting and Destroying Cloud Infrastructure](#deleting-and-destroying-cloud-infrastructure)

## Installation
Clone the repository:
```bash
 git clone https://github.com/DanielSolomon7/GDPR-Project
```

## Setup
Create virtual environment:
```bash
 make create-environment
```

Install packages:
```bash
make install-requirements
```

Run checks on the Lambda Python code - unit, security, and PEP-8:
```bash
make run-checks
```

In the root directory, export PYTHONPATH to the current working directory: export PYTHONPATH=$(pwd)

## Cloud Infrastructure Deployment
Go into the terraform file:
```bash
cd terraform
```

Set up the Terraform files:
```bash
terraform init
```

Plan the Terraform deployment:
```bash
terraform plan
```

Apply the Terraform infrastructure:
```bash
terraform apply
```

## Uploading Unobfuscated CSV File to Storage S3 Bucket
Go into the root directory, and make sure the CSV data file is in the root directory.

Upload the CSV data file to the 'storage' S3 Bucket, by entering in the command line:
```python
python src/run_upload_data_file.py
```
A user input should appear asking you to enter the name of the file - make sure it is the correct name, otherwise an error will occur. If no error occurs, the file has been uploaded.


## Running the Obfuscation Tool and Creating an Obfuscated File
Log into AWS, and run the 'state-machine-for-lambda' state machine - entering a JSON string with a 'file_to_obfuscate' key and a value of a string of the file name, and a 'pii_fields' key, with a value of an array of strings of column names of the desired columns to obfuscate. For example:
```json
{
    "file_to_obfuscate": "people_data.csv",
    "pii_fields": ["name", "email_address"]
}
```

Once run, an obfuscated file, with the chosen columns obfuscated, should be uploaded into the target bucket.

## Deleting and Destroying Cloud Infrastructure
Before running terraform destroy, delete files from the storage and target buckets, by running this command in the root directory:
```bash
python src/run_delete_data_file.py
```
Then enter the name of the file, making sure it is the correct name.

To delete the cloud infrastructure, cd into the terraform folder and run:
```bash
terraform destroy
```
