# GDPR-Project

If uploading file in Terraform doesn't work first time, run it again.
Created upload_data_file_function - run function in root directory: python src/run_upload_data_file.py - then enter the name of the file - make sure it is the correct name, otherwise an error will occur. If no error occurs, the file has been uploaded.

When running terraform destroy, delete files from the storage and target buckets.