from src.upload_data_file import upload_data_file

def run_upload_data_file(user_input):
    return upload_data_file(user_input)

run_upload_data_file(input("Enter the name of a file to upload: "))