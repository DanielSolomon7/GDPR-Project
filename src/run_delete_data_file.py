from src.delete_data_file import delete_data_file


def run_delete_data_file(user_input):
    """Takes the user's input of the name of a file to
    delete, to use as a parameter for running the
    delete_data_file function

    Paramaters:
        user_input (str): the name of the file to delete

    Returns:
        the output of running the delete_data_file function with the
        user's input
    """
    return delete_data_file(user_input)


run_delete_data_file(input("Enter the name of a file to delete: "))
