from _typeshed import Incomplete
from selenium.webdriver.common.options import ArgOptions as ArgOptions
from typing import Optional
from webdriver_helper._driver import WebDriver as WebDriver, WebElement as WebElement

DriverType: Incomplete

def get_webdriver(driver_type: DriverType = ..., *, hub: str = ..., version: Incomplete | None = ..., options: Optional[ArgOptions] = ..., service_args: Optional[dict] = ..., capabilities: Optional[dict] = ...) -> WebDriver: ...

debugger: Incomplete
