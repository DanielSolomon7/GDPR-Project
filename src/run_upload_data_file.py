from src.upload_data_file import upload_data_file


def run_upload_data_file(user_input):
    """Takes the user's input of the name of a file to
    upload, to use as a parameter for running the
    upload_data_file function

    Paramaters:
        user_input (str): the name of the file to upload

    Returns:
        the output of running the upload_data_file function with the
        user's input
    """
    return upload_data_file(user_input)


run_upload_data_file(input("Enter the name of a file to upload: "))
