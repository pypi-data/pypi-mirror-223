from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver

from .selenium import ZuiSelenium


class ZuiSeleniumChrome(ZuiSelenium):
    _service: Optional[ChromeService] = None
    _options: Optional[Options] = None
    _selenium: ZuiSelenium
    driver: WebDriver
    is_connected: bool = False

    def set_option(self, host: str = '', port: int = 0, debugger_address: str = '', proxy_url: str = '', binary_location: str = '', detach: bool = False):
        self._options = Options()
        if detach:
            self._options.add_experimental_option("detach", detach)
        if binary_location:
            self._options.binary_location = binary_location
        if host and port:
            debugger_address = debugger_address or f"{host}:{port}"
            self._options.debugger_address = debugger_address
        if proxy_url:
            self._options.add_argument(f'--proxy-server={proxy_url}')
        return self._options
    # def set_option(self, host: str = 'localhost', port: int = 9000, debug_address: str = '') -> None:
    #     if host and port:
    #         debug_address = debug_address or f"{host}:{port}"
    #         self._options = Options()
    #         self._options.debugger_address = debug_address

    def set_service(self, executable_path: str, port: int = 0) -> None:
        '''
        - Use in case chrome upgrate to latest version but chrome driver is not released
        - Selenium not support that due to chrome driver not exist, so need manually download chrome driver and inject to selenium
        @executable_path: path to executable chrome driver
        - check here for prod released: https://chromedriver.chromium.org/downloads
        - check here for lastest testing released: https://googlechromelabs.github.io/chrome-for-testing
        '''
        if executable_path:
            self._service = ChromeService(executable_path, port)

    def connect(self):
        self.driver = webdriver.Chrome()
        return self.driver

    def connect_debug(self, host: str = 'localhost', port: int = 9000, debug_address: str = '', executable_path: str = '', time_to_wait: float = 0):
        '''
        @port: port number, default `9000`
        @debug_address: format `127.0.0.1:9000`, default `localhost:{port}`
        - Use for case need authorization, you just need to start `chrome beta` -> login account -> close browswer then
            - start `chrome` on debug mode -> call this method to connect to browser opened
        1. Install `chrome beta` for better automation: https://www.google.com/chrome/beta
        2. Start `chrome` by command: `google-chrome-beta --remote-debugging-port={port}`
                - `port` must the same with input parameter of this method
        '''
        if not self.is_connected:
            self.set_option(host, port, debug_address)
            self.set_service(executable_path, port)

            self.driver = webdriver.Chrome(
                options=self._options, service=self._service)  # type: ignore
            if time_to_wait:
                self.driver.set_page_load_timeout(time_to_wait)
            self.is_connected = True
        return self.driver

    def connect_instance(self, proxy_url: str = '', executable_path: str = '', time_to_wait: float = 0, binary_location: str = '', detach: bool = False) -> ZuiSelenium:
        self.set_option(proxy_url=proxy_url,
                        binary_location=binary_location, detach=detach)
        self.set_service(executable_path)

        self.driver = webdriver.Chrome(
            options=self._options, service=self._service)  # type: ignore
        if time_to_wait:
            self.driver.set_page_load_timeout(time_to_wait)

        self._selenium = ZuiSelenium(self.driver)
        return self._selenium

    def connect_multiple_instance(self, count: int = 1):
        drivers = [self.connect_instance() for _ in range(count)]
        return drivers
