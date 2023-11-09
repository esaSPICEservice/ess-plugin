import os


def get_output_folder():
    output_folder = os.path.abspath(os.path.join('.', 'output'))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder