# GDPR-Project

Create virtual environment: python -m venv venv

Activate virtual environment: source venv/bin/activate

In the root directory, export PYTHONPATH to the current working directory: export PYTHONPATH=$(pwd)

Go into terraform file: cd terraform

Set up the Terraform files: terraform init

Plan the Terraform deployment: terraform plan

Apply the Terraform infrastructure: terraform apply

Go back into the root directory

Make sure the CSV data file is in the root directory.

In the root directory, upload the CSV data file: python src/run_upload_data_file.py - then enter the name of the file - make sure it is the correct name, otherwise an error will occur. If no error occurs, the file has been uploaded.

Before running terraform destroy, delete files from the storage and target buckets. Run function in root directory: python src/run_delete_data_file.py - then enter the name of the file - make sure it is the correct name.

To delete the cloud infrastrcuture, cd into the terraform folder and run: terraform destroy.