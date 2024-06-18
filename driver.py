from selenium import webdriver


def get_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-proxy-certificate-handler')
    options.add_argument('--disable-content-security-policy')
    options.add_argument('--start-maximized')
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=options)
    # driver.set_window_size(800, 600)
    return driver
