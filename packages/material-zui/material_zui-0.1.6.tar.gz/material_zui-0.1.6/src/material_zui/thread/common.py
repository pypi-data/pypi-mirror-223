
from typing import Any, Callable


def do_until_success(*callables: Callable[[], Any | bool]) -> None:
    '''
    Execute each callable until 1 success then stop
    '''
    for callable in callables:
        try:
            callable()
            break
        except:
            pass

# def remove():
#     for thread in threads:
#         if not thread.is_alive():
#             threads.discard(thread)
#             number_thread_need_to_add += 1
