import os
from anyio import Path

from material_zui.list import map_to, filter_to, sort_alphabetically
from .type import ZuiFile


def get_names(directory_path: str, is_sort: bool = True, limit: int = 0) -> list[str]:
    '''
    Get all file names in a directory
    '''
    paths = os.listdir(directory_path)
    paths = sort_alphabetically(paths) if is_sort else paths
    return paths[:limit] if limit else paths


def get_file_names(directory_path: str, is_sort: bool = True, limit: int = 0) -> list[str]:
    '''
    Get all file names in a directory
    '''
    file_names = get_names(directory_path, is_sort)
    file_names = filter_to(file_names, lambda file_name,
                           _: is_file(file_name))
    return file_names[:limit] if limit else file_names


def get_paths(directory_path: str, is_sort: bool = True, limit: int = 0) -> list[str]:
    filenames = get_names(directory_path, is_sort, limit)
    return [os.path.join(directory_path, filename) for filename in filenames]


def get_file_info(file_path: str) -> ZuiFile:
    """
    The function takes a file path as input and returns information about the file such as its name,
    extension, and directory name.

    @param file_path: A string representing the path to a file
    @type file_path: str
    @return: A dictionary containing information about the file specified by the input file path. The
    dictionary includes the file name, name (without extension), directory name, and file extension.
    """
    path = Path(file_path)
    file_name = path.name
    name = path.stem
    ext = os.path.splitext(file_path)[1][1:]
    dir_name = os.path.dirname(file_path)
    return {'file_name': file_name, 'name': name, 'dir_name': dir_name, 'ext': ext}


def get_files_info(directory_path: str, ext: str = '', is_sort: bool = True, limit: int = 0) -> list[ZuiFile]:
    """
    Returns a list of file information for all files in the specified directory path with the given file extension (if provided). 

    :param directory_path: A string representing the path to the directory to search for files.
    :param ext: An optional string representing the file extension to filter files by.
    :return: A list of ZuiFile objects containing information about each file in the directory (if no extension provided) or only files with the specified extension.
    """
    files_info = map_to(get_paths(directory_path, is_sort),
                        lambda file_path, _: get_file_info(file_path))
    files_info = filter_to(
        files_info, lambda file_info, _: file_info['ext'] == ext) if ext else files_info
    return files_info[:limit] if limit else files_info


def is_file(file_name: str) -> bool:
    return bool(file_name) and len(file_name.split('.')) == 2
