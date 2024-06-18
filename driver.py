from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def get_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-proxy-certificate-handler')
    options.add_argument('--disable-content-security-policy')
    options.add_argument('--start-maximized')
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(
        options=options,
        service=webdriver.ChromeService(
            ChromeDriverManager().install()
        )
    )
    return driver
