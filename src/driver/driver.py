from selenium import webdriver

def get_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-proxy-certificate-handler')
    chrome_options.add_argument('--disable-content-security-policy')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(
        executable_path='./bin/chromedriver.exe',
        chrome_options=chrome_options
    )
    driver.set_window_size(800, 600)
    return driver