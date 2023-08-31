import time
from .. import driver

class Parser:
    def __init__(self) -> None:
        self.driver = driver.get_driver()

    def wait(self, method):
        time.sleep(5)
        return driver.WebDriverWait(
            self.driver,
            20,
            2
        ).until(
            method
        )

    def wait_element(self, by: str, value: str) -> driver.WebElement:
        return self.wait(driver.EC.presence_of_element_located((by, value)))
    
    def click_element(self, by: str, value: str):
        for i in range(5):
            time.sleep(1)
            try:
                self.wait_element(by, value).click()
                return
            except:
                pass

    def login(self):
        self.driver.get('http://lk.rosreestr.ru/request-access-egrn/property-search')
        try:
            self.driver.find_element(driver.By.ID, 'details-button').click()
            self.driver.find_element(driver.By.ID, 'proceed-link').click()
        except:
            pass

    def request_EGRN(self, value: str):
        self.driver.get('https://lk.rosreestr.ru/request-access-egrn/')
        self.click_element(driver.By.CSS_SELECTOR, 'a[href="/request-access-egrn/property-search"]')
        self.wait_element(driver.By.CSS_SELECTOR, 'input[type=text]').send_keys(value)
        self.click_element(driver.By.CLASS_NAME, 'rros-ui-lib-table__row')
        self.click_element(driver.By.CLASS_NAME, 'build-card-wrapper__header-wrapper__action-button')
        self.click_element(driver.By.CLASS_NAME, 'rros-ui-lib-link_inherit')
