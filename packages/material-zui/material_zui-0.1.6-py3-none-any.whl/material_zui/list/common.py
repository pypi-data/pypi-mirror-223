import random
from random import sample
from typing import Any, Callable, TypeVar

T = TypeVar('T')

R = TypeVar('R')


def is_last_index(list: list[Any], index: int) -> bool:
    return index == len(list) - 1


def list_range(list: list[T], limit: int = 0, start_index: int = 0) -> list[T]:
    end_index = start_index+limit
    return list[start_index:end_index] if end_index else list


def map_to(items: list[T], handle_function: Callable[[T, int], R]) -> list[R]:
    return list(map(handle_function, items, range(len(items))))


def filter_to(items: list[T], handle_function: Callable[[T, int], bool]) -> list[T]:
    result: list[T] = []
    for index, item in enumerate(items):
        if handle_function(item, index):
            result.append(item)
    return result


def get_diff(list1: list[T], list2: list[T]) -> list[T]:
    """Get the difference between two lists.
    Args:
        list1 (list): The first list.
        list2 (list): The second list.
    Returns:
        list: item in list1 not in list2
    """
    return filter_to(list1, lambda item, _: item not in list2)


def get(index: int, default_value: Any = None) -> Callable[[list[Any]], Any | None]:
    """
    The `get` function returns a lambda function that retrieves an item from a list at a given index,
    with an optional default value if the index is out of range.
    @param index: An integer representing the index of the item we want to retrieve from the list
    @type index: int
    @param default_value: The `default_value` parameter is an optional parameter that specifies the
    value to be returned if the index is out of range. If no `default_value` is provided, it defaults to
    `None`
    @type default_value: Any
    @return: A callable function is being returned.
    """
    return lambda items: items[index] if index > -1 and index < len(items) else default_value


def random_sort(value: list[T]) -> list[T]:
    """
    Randomly sorts the elements of a list, but does not change the original list
    """
    return sample(value, len(value))


def flat(input_list: list[list[T]], dept: int = 1) -> list[T]:
    flat_list = []
    for item in input_list:
        if isinstance(item, list):  # type: ignore
            flat_list.extend(flat(item, dept+1))  # type: ignore
        else:
            flat_list.append(item)
    return flat_list


def flat_fp(dept: int = 1) -> Callable[[list[list[T]]], list[T]]:
    '''
    Flat list by functional programming style
    '''
    def wrapper(input_list: list[list[T]]) -> list[T]:
        return flat(input_list, dept)
    return wrapper


def reverse(items: list[T]) -> list[T]:
    '''
    immutable function to reverse a list
    '''
    result = items.copy()
    result.reverse()
    return result


# def random_items(items: list[T], number_of_items: int = 1, is_unique: bool = True) -> list[T]:
#     random_items: list[T] = []
#     len_items = len(items)
#     if number_of_items >= len_items:
#         return items
#     for _ in range(number_of_items):
#         random_index = random.randint(0, len_items - 1)
#         random_item = items[random_index]
#         if not is_unique or random_item not in random_items:
#             random_items.append(random_item)
#     return random_items

def random_items(number_of_items: int = 1, is_unique: bool = True) -> Callable[[list[T]], list[T]]:
    def inner(items: list[T]) -> list[T]:
        random_items: list[T] = []
        len_items = len(items)
        if number_of_items >= len_items:
            return items
        for _ in range(number_of_items):
            random_index = random.randint(0, len_items - 1)
            random_item = items[random_index]
            if not is_unique or random_item not in random_items:
                random_items.append(random_item)
        return random_items
    return inner


def sort_alphabetically(items: list[str], is_reverse: bool = False) -> list[str]:
    list_asc = sorted(items, key=str.lower)
    return reverse(items) if is_reverse else list_asc


def is_list(value: Any) -> bool:
    return isinstance(value, list)


# numbers: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# def is_even(number: int) -> bool:
#     return number % 2 == 0
# even_numbers = filter(is_even, numbers)

# class ZuiList:
#     def __init__(self, items: list[T]) -> None:
#         self.list: list[T] = items

#     def map(self, handle_function: Callable[[T], R]) -> list[R]:
#         return list(map(handle_function, self.list))

#     def filter(self, items: list[T], handle_function: Callable[[T], bool]) -> list[T]:
#         return list(filter(handle_function, items))


# ZuiList([1, 2, 3]).map(lambda x: x+1)
