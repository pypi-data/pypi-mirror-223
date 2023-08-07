import os
import platform
from typing import Any, Callable

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from material_zui.fake import random_sleep
from material_zui.list import filter_to, map_to
from material_zui.string import (list_match, remove_bmp_characters,
                                 remove_special_characters, trim_space)
from material_zui.string.common import remove_all
from material_zui.utility import pipe, pipe_list

from .common import safe_find_element

# from selenium.webdriver.chrome.webdriver import WebDriver


class ZuiSelenium:
    # driver: WebDriver
    driver: Any

    def __init__(self, driver: Any = None) -> None:
        self.is_mac = False
        if not any(os_name in platform.platform() for os_name in ["Windows", "Linux"]):
            self.is_mac = True
        if driver:
            self.driver = driver

    # def __init__(self) -> None:
    #     self.is_mac = False
    #     if not any(os_name in platform.platform() for os_name in ["Windows", "Linux"]):
    #         self.is_mac = True

    @property
    def screen_height(self) -> int:
        return self.driver.execute_script("return window.screen.height;")

    @property
    def scroll_height(self) -> int:
        return self.driver.execute_script("return document.body.scrollHeight;")

    @property
    def page_source(self) -> str: return self.driver.page_source

    @property
    def document(self) -> BeautifulSoup:
        return BeautifulSoup(self.driver.page_source, "html.parser")

    @property
    def current_url(self) -> str: return self.driver.current_url

    def get(self, url: str) -> None:
        self.driver.get(url)

    def close(self) -> None:
        self.driver.close()

    def delay(self, sec: float = 0) -> None:
        random_sleep(1, 5, sec)

    def safe_find_element(
            self, by: str = By.ID,
            value: str | None = None,
            parent: Any = None) -> WebElement | None:
        '''
        This is safe find element method
        @return `None` in case not found
        '''
        return safe_find_element(parent if parent else self.driver, by, value)

    def safe_find_element_by_xpath(self, xpath_value: str) -> WebElement | None:
        return self.safe_find_element(By.XPATH, xpath_value)

    def safe_get_text(self, xpath_value: str) -> str:
        element = self.safe_find_element_by_xpath(xpath_value)
        return element.text if element else ''

    def find_element_by_xpath(self, xpath_value: str) -> WebElement: return self.driver.find_element(
        By.XPATH, xpath_value)

    def find_elements_by_xpath(self, xpath_value: str) -> list[WebElement]: return self.driver.find_elements(
        By.XPATH, xpath_value)

    def find_elements_by_class(self, class_value: str) -> list[WebElement]: return self.driver.find_elements(
        By.CLASS_NAME, class_value)

    def scroll_to_end(self) -> None:
        self.driver.execute_script("window.scrollTo(0, {scroll_height});".format(
            scroll_height=self.scroll_height))

    def scroll(self, step_scroll: int) -> None:
        for index in range(step_scroll):
            print(index+1, "Scrolling to", self.scroll_height)
            self.scroll_to_end()
            self.delay()

    def get_urls(self, class_selector: str) -> list[str]:
        '''
        Get video urls by class selector of each video
        '''
        videos = self.document.find_all(
            "div", {"class": class_selector})
        return map_to(videos, lambda video, _: video.a["href"])

    def switch_to_frame(self, xpath_value: str) -> None:
        '''
        @xpath_value: must be end with `frame/iframe` like `//*[@id="main"]/div[2]/div/iframe`
        '''
        frame_element = self.find_element_by_xpath(xpath_value)
        self.driver.switch_to.frame(frame_element)

    def switch_to_default_content(self) -> None:
        '''
        Out to frame/iframe
        '''
        self.driver.switch_to.default_content()

    def upload_file(self, xpath_value: str, video_relative_path: str) -> None:
        '''
        @xpath_value: must be end with `input` like `//*[@id="root"]/div/div/div/div/div/div/div/input`
        @video_relative_path: video relative path, from root project directory
        '''
        file_input = self.find_element_by_xpath(xpath_value)
        abs_path = os.path.abspath(video_relative_path)
        file_input.send_keys(abs_path)

    def click(self, xpath_value: str):
        '''
        Click then return that element
        '''
        element = self.find_element_by_xpath(xpath_value)
        element.click()
        return element

    def wait_click(self, xpath_value: str, delay_time: int = 10, time_to_try: int = 10):
        element = self.wait_get(xpath_value, delay_time, time_to_try)
        element.click()
        return element

    def safe_click(self, xpath_value: str):
        '''
        Safe click element
        '''
        try:
            element = self.safe_find_element_by_xpath(xpath_value)
            if element:
                element.click()
            return element
        except:
            return None

    def send_keys(self, xpath_value: str, key_value: str, clear_before_send_keys: bool = True, delay_time: int = 10, time_to_try: int = 10) -> WebElement | None:
        '''
        Send keys then return that element
        @xpath_value: only valid with element selector can input value
        @clear_before_send_keys:
        - True: clear input before send keys
        - False: value will input after existed value
        '''
        try:
            element = self.wait_get(xpath_value, delay_time, time_to_try)
            # element = self.find_element_by_xpath(xpath_value)
            element.click()
            self.delay(10)
            if clear_before_send_keys:
                element.send_keys(Keys.CONTROL + 'a')
                self.delay()
                element.send_keys(Keys.BACKSPACE)
            self.delay()
            element.send_keys(key_value)
            return element
        except:
            if time_to_try:
                time_to_try -= 1
                return self.send_keys(xpath_value, key_value,
                                      clear_before_send_keys, delay_time, time_to_try)
            return None

    def wait_until(self, condition: Callable[[], bool], delay: int = 0, time_to_try: int = 10) -> None:
        is_continue = time_to_try > 0
        count = 0
        try:
            while is_continue:
                if count > time_to_try:
                    is_continue = False
                count += 1

                if condition():
                    is_continue = False
                self.delay(delay)
        except:
            self.wait_until(condition, delay, time_to_try-count)

    def wait_get(self, xpath_value: str, delay_time: int = 10, time_to_try: int = 10) -> WebElement:
        '''
        - Total wait time of this function is `delay_time x time_to_try`, default is `10x10 = 100 seconds`
        - @delay_time: delay time for each `time_to_try`
        - @time_to_try: how many time to try
        '''
        for _ in range(time_to_try):
            element = self.safe_find_element_by_xpath(xpath_value)
            if element:
                return element
            self.delay(delay_time)
        return WebDriverWait(self.driver, delay_time).until(  # using explicit wait for 10 seconds
            EC.presence_of_element_located(
                (By.XPATH, xpath_value))  # finding the element
        )

    def input_tags(self, tags: list[str], title_element: WebElement | None = None, xpath_value: str = '') -> None:
        title_element = title_element or self.wait_get(xpath_value)
        if tags and len(tags):
            title_element.send_keys(Keys.SPACE)
            for tag in tags:
                title_element.send_keys(tag)
                self.delay()
                title_element.send_keys(Keys.SPACE)

    def split_title(self, title: str) -> dict[{'title': str, 'caption': str, 'yt_description': str, 'tags': list[str], 'hash_tags': list[str]}]:
        '''
        '''
        valid_title = pipe(
            remove_bmp_characters,
            trim_space
        )(title)
        caption = pipe(
            remove_all(r' \#.+'),
            trim_space
        )(valid_title)
        yt_description = remove_all(r'>')(caption)

        raw_tags = pipe_list(remove_special_characters, trim_space)(
            list_match('(#)([^ ]+)', 2)(valid_title.strip('#')))
        tags = filter_to(raw_tags, lambda tag, _: len(tag) > 1)
        hash_tags = map_to(tags, lambda tag, _: f'#{tag}')

        return {
            'title': valid_title,
            'caption': caption,
            'yt_description': yt_description,
            'tags': tags,
            'hash_tags': hash_tags,
        }
