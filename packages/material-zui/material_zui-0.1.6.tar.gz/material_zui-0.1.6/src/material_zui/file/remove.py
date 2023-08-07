import os

from material_zui.list import filter_to

from .common import get_file_names, is_file


def remove_files(directory: str, file_names: list[str]) -> None:
    """
    Removes multiple files from a directory.
    Args:
        directory: The directory to remove the files from.
        file_names: The list of files to remove.
    """
    for file_name in file_names:
        file_path = os.path.join(directory, file_name)
        # print('file_name', directory, file_name)
        if os.path.isfile(file_path):
            if os.path.exists(file_path):
                os.remove(file_path)


def remove_by_order(directory: str, limit: int) -> None:
    """
    Remove number of file by `limit` input from a `directory`, file name sort by alphabetically
    """
    file_names = get_file_names(directory, limit=limit)
    file_names = filter_to(file_names, lambda file_name,
                           _: is_file(file_name))
    remove_files(directory, file_names)
