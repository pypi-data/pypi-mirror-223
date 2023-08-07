from re import compile, finditer
from typing import Any, Callable

from material_zui.list import filter_to, map_to


def list_match(regex: str, group: int = 0) -> Callable[[str], list[str]]:
    '''
    - ex:

    ```py
    list_match('(#)([^ ]+)', 2)("title #tag1 #tag2 #tag3") => ['tag', 'tag2', 'tag3']
    ```
    '''
    pattern = compile(regex)

    def matcher(value: str) -> list[str]:
        items = map_to(list(finditer(pattern, value)),
                       lambda match, _: match.group(group))
        return filter_to(items, lambda item, _: len(item) > 0)
    return matcher


def is_exist(regex: str) -> Callable[[str], bool]:
    pattern = compile(regex)
    return lambda value: bool(pattern.search(value))

# def is_exist(value: str, regex: str) -> bool:
#     pattern = compile(regex)
#     return bool(pattern.search(value))

# def check_substring(string, substring):
#     regex = re.compile(substring)
#     if regex.search(string):
#         return True
#     else:
#         return False


def remove_all(regex_pattern_to_remove: str) -> Callable[[str], str]:
    pattern = compile(regex_pattern_to_remove)
    return lambda text: pattern.sub('', text)


def replace_all(regex_pattern: str, replace_value: str) -> Callable[[str], str]:
    pattern = compile(regex_pattern)
    return lambda text: pattern.sub(replace_value, text)


def remove_special_characters(text: str) -> str:
    """
    The function removes all special characters from a given string.

    @param text: The input text string that may contain special characters
    @type text: str
    @return: The function `remove_special_characters` takes a string `text` as input and removes all
    special characters (i.e., non-alphanumeric characters) from it using a regular expression pattern.
    The function returns the modified string with special characters removed.
    """
    return remove_all('[^\\w\\s]')(text)


def remove_bmp_characters(text: str) -> str:
    """Removes all BMP characters from a string.
    Args:
      text: The string to remove BMP characters from.
    Returns:
      The string with all BMP characters removed.
    """
    return remove_all(r'[^\u0000-\uFFFF]')(text)


def trim_space(text: str) -> str:
    """
    The function takes a string as input, removes any leading or trailing spaces, and replaces any
    consecutive spaces within the string with a single space.

    :param text: A string that may contain extra spaces that need to be trimmed down to a single space
    :type text: str
    :return: The function `trim_space` takes a string `text` as input and returns a new string with all
    consecutive spaces replaced by a single space, and leading/trailing spaces removed.
    """
    return replace_all(r' +', ' ')(text.strip())


def not_empty(value: Any) -> bool:
    return value != None and len(value) > 0


def limit_by_byte(byte_limit: int = 256) -> Callable[[str], str]:
    """Limits the length of a string by byte count.
    Args:
      byte_limit: The maximum number of bytes allowed.
    Returns:
      A function that takes a string and returns the limited string.
    """
    def inner_function(value: str) -> str:
        return value.encode()[:byte_limit].decode() if len(value.encode()) > byte_limit else value
    return inner_function


def count_byte(value: str) -> int: return len(value.encode())


def to_string(value: Any) -> str: return str(value)
