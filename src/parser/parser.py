import time
from .. import driver

class Parser:
    def __init__(self) -> None:
        self.driver = driver.get_driver()

    def wait_element(self, by: str, value: str) -> driver.WebElement:
        time.sleep(5)
        return driver.WebDriverWait(
            driver=self.driver,
            timeout=6,
            poll_frequency=2
        ).until(
            method=driver.EC.presence_of_element_located((by, value))
        )
        
    def check_no_errors(self) -> bool:
        errors = self.driver.find_elements(driver.By.CLASS_NAME, 'rros-ui-lib-error-title')
        if errors == []:
            return True
        for error in errors:
            error.find_element(driver.By.TAG_NAME, 'button').click()
        return False
    
    def click_element(self, by: str, value: str):
        for _ in range(5):
            self.wait_element(by, value).click()
            time.sleep(1)
            if self.check_no_errors():
                return
            time.sleep(2)
        raise

    def login(self):
        self.driver.get('http://lk.rosreestr.ru/request-access-egrn/property-search')
        if self.driver.find_elements(driver.By.ID, 'details-button') != []:
            self.driver.find_element(driver.By.ID, 'details-button').click()
            self.driver.find_element(driver.By.ID, 'proceed-link').click()

    def request_EGRN(self, value: str):
        self.driver.get('https://lk.rosreestr.ru/request-access-egrn/')
        self.click_element(driver.By.CSS_SELECTOR, 'a[href="/request-access-egrn/property-search"]')
        self.wait_element(driver.By.CSS_SELECTOR, 'input[type=text]').send_keys(value)
        self.click_element(driver.By.CLASS_NAME, 'rros-ui-lib-table__row')
        self.click_element(driver.By.CLASS_NAME, 'build-card-wrapper__header-wrapper__action-button')
        self.click_element(driver.By.CLASS_NAME, 'rros-ui-lib-link_inherit')
        return self.wait_element(driver.By.CLASS_NAME, 'success-view').text == 'Ваша заявка отправлена в ведомство'
