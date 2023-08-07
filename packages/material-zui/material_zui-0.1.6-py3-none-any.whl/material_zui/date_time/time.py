# from re import match
# import threading
# import time


# def set_timeout(code, milliseconds):
#     timer = threading.Timer(milliseconds / 1000, code)
#     timer.start()
#     return timer


# def clear_timeout(timer):
#     timer.cancel()


# def my_code():
#     print("Hello World!")


# timer = set_timeout(my_code, 5)


# def set_interval(func, sec):
#     def func_wrapper():
#         set_interval(func, sec)
#         func()
#     # t = threading.Timer(sec, func_wrapper)
#     t = threading.Timer(sec, func)
#     t.start()
#     return t


# def clear_interval(t):
#     print('cancel')
#     t.cancel()


# def print_hello():
#     print("Hello!")


# interval_id = set_interval(print_hello, 1)
# time.sleep(5)
# clear_interval(interval_id)
# print('abc')

# def time_to_seconds(time_str: str) -> int:
#     """
#     Convert a string time to seconds.
#     Args:
#         time_str: The string time to convert.
#         ex: `00:12:34` => `754` seconds
#         ex: `01:23:45` => `5025` seconds
#     Returns:
#         The number of seconds in the string time.
#     """
#     regex = r"^(\d+):(\d+):(\d+)$"
#     match_value = match(regex, time_str)
#     if match_value:
#         hours = int(match_value.group(1))
#         minutes = int(match_value.group(2))
#         seconds = int(match_value.group(3))
#         return 3600 * hours + 60 * minutes + seconds
#     return 0


def time_to_seconds(value: str) -> int:
    """Converts a string time to seconds.
    Args:
      value: A string time in the format HH:MM:SS.
    Returns:
      The number of seconds in the time string.
    - ex: ('00:12:34') => 754
    """
    while len(value.split(":")) < 3:
        value = f'00:{value}'
    hours, minutes, seconds = value.split(":")
    seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    return seconds


def second_to_str_time(seconds: int) -> str:
    """Converts seconds to time in the format HH:MM:SS.
    Args:
      seconds: The number of seconds.

    Returns:
      A string representing the time in the format HH:MM:SS.
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return time_str


def second_to_time(seconds: int) -> dict[{'hours': int, 'minutes': int, 'seconds': int}]:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return {
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds
    }
