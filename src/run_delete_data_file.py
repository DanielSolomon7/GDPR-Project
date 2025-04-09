from src.delete_data_file import delete_data_file


def run_delete_data_file(user_input):
    return delete_data_file(user_input)


run_delete_data_file(input("Enter the name of a file to delete: "))
