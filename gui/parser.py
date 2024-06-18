import time
import re
from enum import Enum
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from PyQt6.QtCore import QThread, pyqtSignal
from driver import get_driver
from database.models import CadastralNumber
from database.database import database


class ParserTask(Enum):
    NONE = 0
    LOGIN = 1
    LOGIN_QR = 2
    LOGIN_ESIGN = 3
    REQUESTS = 4
    CLEAR_DATA = 5
    LOAD_DATA = 6
    DOWNLOAD_DATA = 7


class ParserThread(QThread):
    indicators = pyqtSignal(int, int, int, int)
    current_cadastral_number = pyqtSignal(str)
    
    def __init__(self, parent):
        super().__init__(parent)
        self.driver = get_driver()
        self.task = ParserTask.NONE
        self.ESIA_login = ''
        self.ESIA_password = ''
        self.data_filename = ''
    
    def run(self):
        match self.task:
            case ParserTask.LOGIN_QR:
                self.login_qrCode()
            case ParserTask.LOGIN:
                self.login(self.ESIA_login, self.ESIA_password)
            case ParserTask.LOGIN_ESIGN:
                self.login_ESigrature()
            case ParserTask.REQUESTS:
                self.requests()
            case ParserTask.CLEAR_DATA:
                self.clear_data()
            case ParserTask.LOAD_DATA:
                self.load_data(self.data_filename)
            case ParserTask.DOWNLOAD_DATA:
                self.download()
        self.task = ParserTask.NONE
    
    def update_indicators(self):
        database.connect(True)
        status = CadastralNumber.get_status()
        self.indicators.emit(status.new, status.sent, status.error, status.downloaded)
        database.close()

    def _wait_element(self, value: str, *, by: str = By.CSS_SELECTOR, timeout: int = 5, poll_frequency: int = 1):
        try:
            return WebDriverWait(
                driver=self.driver, timeout=timeout, poll_frequency=poll_frequency
            ).until(method=EC.presence_of_element_located((by, value)))
        except TimeoutException:
            return None
    
    def _is_cadastral_number(self, value: str) -> bool:
        return bool(re.match(r'\d{2}:\d{2}:\d{6,7}:\d*', value))
    
    def login(self, login: str, password: str):
        self.driver.get('http://lk.rosreestr.ru/request-access-egrn/property-search')
        self._wait_element('div.login-link').click()
        self._wait_element('input#login').send_keys(login)
        self._wait_element('input#password').send_keys(password)
        self._wait_element('//button[text()=" Войти "]', by=By.XPATH).click()
    
    def login_qrCode(self):
        self.driver.get('http://lk.rosreestr.ru/request-access-egrn/property-search')
        self._wait_element('div.login-link').click()
        self._wait_element('//button[text()=" QR-код "]', by=By.XPATH).click()
    
    def login_ESigrature(self):
        self.driver.get('http://lk.rosreestr.ru/request-access-egrn/property-search')
        self._wait_element('div.login-link').click()
        self._wait_element('//button[text()=" Эл. подпись "]', by=By.XPATH).click()
    
    def request_EGRN(self, cadastral_number: str) -> bool:
        if not self._is_cadastral_number(cadastral_number):
            return False
        self.driver.get('https://lk.rosreestr.ru/request-access-egrn/property-search')
        for _ in range(5):
            try:
                self._wait_element('input[type="text"]').send_keys(cadastral_number)
                if self._wait_element('//li[text()="Превышен лимит обращений, попробуйте позже"]',
                                      by=By.XPATH, timeout=2):
                    raise
                self._wait_element('div.on-search-tab div[role="rowgroup"]').click()
                self._wait_element('button[data-cy="RealEstateObjectCard.action-button"]').click()
                self._wait_element('div.rros-ui-lib-link').click()
                return bool(self._wait_element('div.success-view__success-message'))
            except:
                time.sleep(5)
                self.driver.refresh()
        return False
    
    def load_data(self, filename):
        database.connect(True)
        with open(filename, 'r', encoding='utf-8') as file:
            while line := file.readline():
                try:
                    CadastralNumber.create(
                        cadastral_number=line.rstrip(),
                        status='new'
                    )
                except:
                    pass
        self.update_indicators()
        database.close()
    
    def clear_data(self):
        database.connect(True)
        CadastralNumber.delete().execute()
        self.update_indicators()
        database.close()
    
    def requests(self):
        database.connect(True)
        cadastral_number = CadastralNumber.get_or_none(CadastralNumber.status == 'new')
        while cadastral_number:
            self.current_cadastral_number.emit(cadastral_number.cadastral_number)
            if self.request_EGRN(cadastral_number.cadastral_number):
                cadastral_number.status = 'sent'
            else:
                cadastral_number.status = 'error'
            cadastral_number.save()
            self.update_indicators()
            cadastral_number = CadastralNumber.get_or_none(CadastralNumber.status == 'new')
        self.current_cadastral_number.emit('')
        database.close()
    
    def download(self):
        database.connect(True)
        download_url = 'https://lk.rosreestr.ru/request-access-egrn/my-claims'
        self.driver.get(download_url)
        rowgroup = self._wait_element('div[role="rowgroup"]')
        next_button = self.driver.find_element(By.CSS_SELECTOR, 'button.rros-ui-lib-table-pagination__btn--next')
        while next_button.get_attribute('disabled') is None:
            for row in rowgroup.find_elements(By.CSS_SELECTOR, 'div[role="row"]'):
                status = row.find_element(By.CSS_SELECTOR, 'div[data-test-id="cell-4"]').text
                if status != 'Выполнено':
                    continue
                cadastral_number = CadastralNumber.get_or_none(
                    CadastralNumber.status == 'sent',
                    CadastralNumber.cadastral_number == row.find_element(By.CSS_SELECTOR, 'div[data-test-id="cell-2"]').text
                )
                if cadastral_number:
                    row.find_element(By.TAG_NAME, 'a').click()
                    cadastral_number.status = 'downloaded'
                    cadastral_number.save()
                    self.update_indicators()
                    time.sleep(10)
            next_button.click()
            time.sleep(1)
        database.close()
