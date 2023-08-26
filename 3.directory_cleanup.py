import os

def list_txt_files(directory: str = ".") -> list[str]:
    """
    List all .txt files in the given directory.

    Args:
        directory (str): Path of the directory to search. Defaults to the current directory.

    Returns:
        list[str]: List of .txt files in the directory.
    """
    files_in_directory = os.listdir(directory)
    return [file for file in files_in_directory if file.endswith(".txt")]

def delete_files(files: list[str]) -> None:
    """
    Delete the given list of files.

    Args:
        files (list[str]): List of file paths to delete.
    """
    for file in files:
        try:
            os.remove(file)
            print(f"Deleted {file}")
        except OSError as e:
            print(f"Unable to delete {file}. Reason: {e.strerror}")

if __name__ == "__main__":
    txt_files = list_txt_files()
    delete_files(txt_files)
