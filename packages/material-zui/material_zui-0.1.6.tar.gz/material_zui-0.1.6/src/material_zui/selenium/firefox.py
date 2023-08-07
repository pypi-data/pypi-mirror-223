from typing import Optional

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver

from .selenium import ZuiSelenium


class ZuiSeleniumFirefox(ZuiSelenium):
    _driver: WebDriver
    _selenium: ZuiSelenium
    _options: Optional[Options] = None
    is_connected: bool = False

    def connect(self):
        self._driver = webdriver.Firefox()
        return self._driver

    # def connect_debug(self, port: int = 9000, debug_address: str = ''):
    #     '''
    #     @port: port number, default `9000`
    #     @debug_address: format `127.0.0.1:9000`, default `localhost:{port}`
    #     - Use for case need authorization, you just need to start `chrome beta` -> login account -> close browswer then
    #         - start `chrome` on debug mode -> call this method to connect to browser opened
    #     1. Install `chrome beta` for better automation: https://www.google.com/chrome/beta
    #     2. Start `chrome` by command: `google-chrome-beta --remote-debugging-port={port}`
    #             - `port` must the same with input parameter of this method
    #     '''
    #     if not self.is_connected:
    #         debug_address = debug_address or f"localhost:{port}"
    #         self.options = Options()
    #         self.options.add_experimental_option(
    #             "debuggerAddress", debug_address)
    #         self.driver = webdriver.Firefox(options=self.options)
    #         self.is_connected = True
    #     return self.driver

    def set_option(self, proxy_url: str):
        if proxy_url:
            self._options = Options()
            self._options.add_argument(f'--proxy-server={proxy_url}')
            # if self._driver:
            #     self._driver.options = self._options
        return self._options

    def connect_instance(self, proxy_url: str = '') -> ZuiSelenium:
        self.set_option(proxy_url)
        self._driver = webdriver.Firefox(options=self._options)  # type: ignore
        self._selenium = ZuiSelenium(self._driver)
        return self._selenium
    # def connect_instance(self, proxy_url: str = '') -> ZuiSelenium:
    #     self._driver = webdriver.Firefox()
    #     self.set_option(proxy_url)
    #     self._selenium = ZuiSelenium(self._driver)
    #     return self._selenium

    # def connect_instance(self, proxy_url: str = ''):
    #     proxy_url = 'http://59.124.240.22:3128'
    #     options = Options()
    #     options.add_argument(f'--proxy-server={proxy_url}')
    #     self._driver = webdriver.Firefox(options)
    #     self._driver.options = options
    #     return ZuiSelenium(webdriver.Firefox(options))

    def connect_multiple_instance(self, count: int = 1):
        drivers = [self.connect_instance() for _ in range(count)]
        return drivers
