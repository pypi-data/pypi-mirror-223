from typing import Any, Callable
from urllib.parse import urlparse

import requests
from fp.fp import FreeProxy

from material_zui.fake import random_sleep
from material_zui.string import to_string


def is_valid_url(url: str) -> bool:
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme and parsed_url.netloc)


# def is_proxy_working(proxy_url: str, timeout: int | None = None) -> dict[str, Any] | None:
    # try:
    #     check_host = 'https://httpbin.org/ip'
    #     response = requests.get(check_host, proxies={
    #                             "http": proxy_url, "https": proxy_url}, timeout=timeout)
    #     return response.json()
    # except:
    #     return None

def is_proxy_working(proxy_url: str, timeout: int | None = 10) -> bool:
    try:
        response = requests.get("https://www.google.com",
                                proxies={"http": f'http://{proxy_url}', "https": f'https://{proxy_url}'}, timeout=timeout)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False


def proxies_working(urls: list[str], timeout: int | None = 20):
    results: list[dict[str, Any]] = []
    for url in urls:
        result = is_proxy_working(url, timeout)
        print(url, result)
        if result:
            results.append(result)
    return results


def proxies_working_fp(timeout: int | None = None) -> Callable[[list[str]], list[dict[str, Any]]]:
    def inner(urls: list[str]) -> list[dict[str, Any]]:
        return proxies_working(urls, timeout)
    return inner


# def proxies(urls: list[str]):
#     current_urls = set(urls)

#     def get_next():
#         is_proxy_working(current_urls.pop())
#     return ''


def get_proxy_working(elite: bool = True, timeout: float = 1, https: bool = True, unique: bool = False) -> str:
    free_proxy = FreeProxy(elite=elite, timeout=timeout, https=https)
    is_valid = False
    proxy_url: str = ''
    count = 0
    proxies: set[str] = set()
    while not is_valid:
        proxy = free_proxy.get()
        proxy_url = to_string(proxy)
        if not unique or proxy_url not in proxies:
            proxies.add(proxy_url)
            is_valid = is_proxy_working(proxy_url, 20)
            count += 1
            print(count, proxy_url, is_valid)
        if not is_valid:
            random_sleep()
    return proxy_url

# def get_proxy_working(elite: bool = True, timeout: float = 1, https: bool = True, unique: bool = False) -> str:
#     free_proxy = FreeProxy(elite=elite, timeout=timeout, https=https)
#     is_valid = False
#     proxy_url: str = ''
#     count = 0
#     proxies: set[str] = set()
#     while not is_valid:
#         proxy = free_proxy.get()
#         proxy_url = to_string(proxy)
#         if proxy_url not in proxies:
#             proxies.add(proxy_url)
#             is_valid = is_proxy_working(proxy_url, 20)
#             count += 1
#             print(count, proxy_url, is_valid)
#         else:
#             random_sleep()
#     return proxy_url
