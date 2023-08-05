import importlib
import inspect
import logging
import pkgutil

from pydantic import BaseModel
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

logger = logging.getLogger("nomnomdata.SignInBase")


def get_sign_in_class_for(domain: str):
    base_class = SignInBase
    plugins_name = "nnd_app_sdk.signin.signins"
    plugins_package = importlib.import_module(plugins_name)

    sign_in_classes = []
    for _, module_name, _ in pkgutil.walk_packages(plugins_package.__path__):
        # import module
        full_module_name = f"{plugins_name}.{module_name}"
        module = importlib.import_module(full_module_name)

        # get all classes defined in the module
        for name, obj in inspect.getmembers(module):
            if (
                inspect.isclass(obj)
                and issubclass(obj, base_class)
                and obj is not base_class
            ):
                sign_in_classes.append(obj)

    # find class that matches domain
    for sign_in_class in sign_in_classes:
        if sign_in_class.domain == domain:
            return sign_in_class

    domains = ", ".join([sign_in_class.domain for sign_in_class in sign_in_classes])
    raise Exception(
        f'Sign in class for domain "{domain}" not found. Available domains: {domains}'
    )


class WebCredentials(BaseModel):
    domain: str = ""
    username: str
    password: str


class SignInBase:
    """
    Base class for creating sign in classes. Use case is to gather credentials
    from domains in agnostic manner, in order to utilize the provided cookies
    by e.g. `requests` library.

    Classes that inherit form SignInBase should:
    * declare a class level `domain` variable that should contain the domain
    for which the class is responsible for signing in e.g. 'bonfire.com'
    * declare a method `domain_sign_in` that successfully signs in to the `domain`

    Example usage:
    ```python
    import requests

    from base import get_sign_class_for

    # grab class responsible for signing into bonfire
    sign_in_class = get_sign_class_for('bonfire.com')
    # sign in to bonfire
    sign_in_instance = sign_in_class({
        "username": "username to use to connect",
        "password": "password to use to connect",
    })
    # sign in & get cookies
    cookies = sign_in_instance.sign_in()

    # create a requests session, and copy over the cookies from selenium
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # now, should be able to access url with requests library
    image_url = 'https://pd.bonfire.com//download/ba9fd376-4554-4a0c-b250-899a07392fbe/png/'
    image_response = session.get(image_url)
    ```
    """

    def __init__(self, parameters: dict):
        """`parameters` dictionary, should contain `username` & `password` and
        will be validated by WebCredentials BaseModel."""
        self.credentials = WebCredentials(**parameters)

        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--headless")
        options.add_argument("--remote-debugging-port=9222")

        self.driver = webdriver.Chrome(
            service=ChromiumService(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            ),
            options=options,
        )

    def wait_for(self, xpath: str, timeout: int = 10):
        wait = WebDriverWait(self.driver, timeout)
        try:
            element = wait.until(
                expected_conditions.presence_of_element_located((By.XPATH, xpath))
            )
        except TimeoutException as e:
            logger.error(
                f"Timed out while waiting for XPATH {xpath} in source:"
                "\n"
                f"{self.driver.page_source}"
            )
            raise e

        return element

    def sign_in(self):
        """Returns the cookies after a succesful sign in."""
        self.domain_sign_in()

        return self.driver.get_cookies()

    def domain_sign_in(self):
        raise NotImplementedError
