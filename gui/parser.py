import re
from enum import Enum
from typing import Sequence
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
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

    def _wait_element(self, value: str, *, by: str = By.CSS_SELECTOR, timeout: float = 5, poll_frequency: float = 1):
        try:
            return WebDriverWait(
                driver=self.driver, timeout=timeout, poll_frequency=poll_frequency
            ).until(method=EC.presence_of_element_located((by, value)))
        except TimeoutException:
            return None
    
    def _is_cadastral_number(self, value: str) -> bool:
        return bool(re.match(r'\d{2}:\d{2}:\d{6,7}:\d*', value))
    
    def close_errors(self):
        try:
            for close_button in self.driver.find_elements(By.CSS_SELECTOR, '.rros-ui-lib-error button'):
                close_button.click()
        except:
            pass
    
    def click_login_button(self):
        try:
            self._wait_element('div.login-link').click()
        except:
            self.close_errors()
            self._wait_element('div.login-link').click()
        
    def login(self, login: str, password: str):
        self.driver.get('http://lk.rosreestr.ru/request-access-egrn/property-search')
        self.click_login_button()
        self._wait_element('input#login').send_keys(login)
        self._wait_element('input#password').send_keys(password)
        self._wait_element('//button[text()=" Войти "]', by=By.XPATH).click()
        self.driver.get_cookies()
    
    def login_qrCode(self):
        self.driver.get('http://lk.rosreestr.ru/request-access-egrn/property-search')
        self.click_login_button()
        self._wait_element('//button[text()=" QR-код "]', by=By.XPATH).click()
    
    def login_ESigrature(self):
        self.driver.get('http://lk.rosreestr.ru/request-access-egrn/property-search')
        self.click_login_button()
        self._wait_element('//button[text()=" Эл. подпись "]', by=By.XPATH).click()
    
    def request_EGRN(self, cadastral_number: str) -> bool:
        for _ in range(2):
            try:
                self.driver.get('https://lk.rosreestr.ru/request-access-egrn/property-search')
                number_input = self._wait_element('input[type="text"]')
                number_input.send_keys(cadastral_number)
                if not self._wait_element(f'//a[text()="{cadastral_number}"]', by=By.XPATH):
                    raise
                for __ in range(3):
                    number_input.send_keys(';')
                    if self._wait_element('ul.rros-ui-lib-error-content', timeout=1.5, poll_frequency=0.3):
                        self.close_errors()
                        self.sleep(3)
                        continue
                    self._wait_element('button[data-cy="RealEstateObjectCard.action-button"]').click()
                    self._wait_element('//div[text()="Запросить сведения об объекте"]', by=By.XPATH).click()
                    return bool(self._wait_element('div#success-view'))
            except:
                self.driver.refresh()
        return False
    
    def load_data(self, filename):
        database.connect(True)
        with open(filename, 'r', encoding='utf-8') as file:
            while line := file.readline():
                data = line.rstrip()
                if not self._is_cadastral_number(data):
                    continue
                try:
                    CadastralNumber.create(cadastral_number=data, status='new')
                except:
                    pass
        self.update_indicators()
        database.close()
    
    def clear_data(self):
        database.connect(True)
        CadastralNumber.delete().execute()
        self.update_indicators()
        database.close()
    
    def get_cadastral_number(self) -> CadastralNumber | None:
        return CadastralNumber.get_or_none(CadastralNumber.status == 'new') \
            or CadastralNumber.get_or_none(CadastralNumber.status == 'error')
    
    def requests(self):
        database.connect(True)
        cadastral_number = self.get_cadastral_number()
        while cadastral_number:
            self.current_cadastral_number.emit(cadastral_number.cadastral_number)
            if self.request_EGRN(cadastral_number.cadastral_number):
                cadastral_number.status = 'sent'
            else:
                cadastral_number.status = 'error'
            cadastral_number.save()
            self.update_indicators()
            cadastral_number = self.get_cadastral_number()
            self.sleep(3)
        self.current_cadastral_number.emit('')
        database.close()
    
    def get_download_urls(self) -> dict[str, str]:
        download_urls = {}
        params = '''{
            credentials: "same-origin",
            method: "POST",
            headers: {
                "Content-Type": "application/json;charset=utf-8"
            },
            body: JSON.stringify({
                "requestNumber": "",
                "cadastralNumber": "",
                "startDate": null,
                "endDate": null
            })
        }'''
        page = 0
        while True:
            script = f'''
                var callback = arguments[arguments.length - 1];
                fetch("https://lk.rosreestr.ru/account-back/applications?page={page}&size=10", {params})
                    .then(response => response.json())
                    .then(data => callback(data));
            '''
            response = self.driver.execute_async_script(script)
            if response.get('numberOfElements') is None:
                self.sleep(1)
                continue
            if response.get('numberOfElements') == 0:
                break
            for item in response.get('content', []):
                if item.get('statusCode') == 'processed':
                    cadastralNumber = item.get('cadastralNumber')
                    if cadastralNumber in download_urls:
                        continue
                    download_urls[cadastralNumber] = f'https://lk.rosreestr.ru/account-back/applications/{item.get("id")}/download'
            page += 1
        return download_urls
    
    def open_download_page(self, cadastral_number: CadastralNumber):
        self.driver.switch_to.window(self.main_tab)
        url = self.download_urls.get(cadastral_number.cadastral_number)
        if url is None:
            return
        script = f'window.open("{url}", "_blank");'
        self.driver.execute_script(script)
        self.download_tabs[self.driver.window_handles[-1]] = cadastral_number
        self.driver.switch_to.window(self.main_tab)
    
    def download(self):
        database.connect(True)
        self.current_cadastral_number.emit('Скачивание')
        
        self.download_urls = self.get_download_urls()
        self.download_tabs: dict[str, CadastralNumber] = {}
        self.main_tab = self.driver.window_handles[0]
        
        for cadastral_number in CadastralNumber.select().where(CadastralNumber.status == 'sent'):
            self.open_download_page(cadastral_number)
        while self.download_tabs:
            for tab, cadastral_number in self.download_tabs.copy().items():
                if tab not in self.driver.window_handles:
                    cadastral_number.status = 'downloaded'
                    cadastral_number.save()
                    self.download_tabs.pop(tab)
                    continue
                self.driver.switch_to.window(tab)
                self.driver.close()
                self.open_download_page(cadastral_number)
            self.update_indicators()
            if not self.download_tabs:
                break
            self.sleep(60 * 2)
        self.current_cadastral_number.emit('')
        database.close()
