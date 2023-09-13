import time
from datetime import datetime
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

    def request_EGRN(self, value: str) -> str:
        try:
            self.driver.get('https://lk.rosreestr.ru/request-access-egrn/')
            self.click_element(driver.By.CSS_SELECTOR, 'a[href="/request-access-egrn/property-search"]')
            self.wait_element(driver.By.CSS_SELECTOR, 'input[type=text]').send_keys(value)
            self.click_element(driver.By.CLASS_NAME, 'rros-ui-lib-table__row')
            self.click_element(driver.By.CLASS_NAME, 'build-card-wrapper__header-wrapper__action-button')
            self.click_element(driver.By.CLASS_NAME, 'rros-ui-lib-link_inherit')
            if self.wait_element(driver.By.CLASS_NAME, 'success-view').text == 'Ваша заявка отправлена в ведомство':
                return 'sent'
        except Exception as e:
            with open('bin/exceptions.txt', 'a', encoding='utf-8') as logfile:
                logfile.write(f'[{datetime.now()}] ERROR: {e}')
        return 'error'
    
    def collect_EGRN(self, cadastral_number: str) -> str:
        self.driver.get('https://lk.rosreestr.ru/request-access-egrn/my-claims')
        while True:
            time.sleep(2)
            next_button = self.wait_element(driver.By.CSS_SELECTOR, 'button.rros-ui-lib-table-pagination__btn--next')
            if next_button.get_attribute('disabled'):
                break
            self.wait_element(driver.By.CLASS_NAME, 'rros-ui-lib-table__row')
            for element in self.driver.find_elements(driver.By.CLASS_NAME, 'rros-ui-lib-table__row'):
                _cadastral_number = element.find_element(driver.By.CSS_SELECTOR, 'div[data-test-id="cell-2"]').text
                if _cadastral_number == cadastral_number:
                    try:
                        element.find_element(driver.By.TAG_NAME, 'a').click()
                        time.sleep(1)
                        return 'downloaded'
                    except:
                        return 'loaded'
            next_button.click()
        return 'not find'
