import os
import time

from django.conf import settings

import pytest
from freezegun import freeze_time
from libfaketime import fake_time, reexec_if_needed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

reexec_if_needed()

USER_DATA = {
    "email": "ohrstrom+obr-e2e@gmail.com",
}

CARD_DATA = {
    "number": 4242424242424242,
    "expiry": 1222,
    "cvc": 123,
}


def fill_form(driver, values):
    for value in values:
        path = value[0]
        content = value[1]
        el = driver.find_element(By.XPATH, path)
        el.send_keys(content)
        time.sleep(0.2)


@pytest.fixture(scope="class")
def driver_init(request):
    options = Options()
    if not os.environ.get("TEST_E2E_DISABLE_HEADLESS"):
        options.add_argument("--headless")
    # options.add_argument("--auto-open-devtools-for-tabs")
    os.makedirs("screenshots", exist_ok=True)
    driver = webdriver.Chrome(options=options)
    driver.set_window_position(0, 0)
    driver.set_window_size(1200, 900)
    driver.implicitly_wait(20)
    request.cls.driver = driver
    yield
    driver.close()


@pytest.mark.django_db
@pytest.mark.e2e
@pytest.mark.usefixtures("driver_init")
# @freeze_time("2021-01-01 00:00:00", tz_offset=0)
class TestAccount:
    def test_signup(self, live_server, settings, mailoutbox):
        settings.SITE_URL = live_server.url
        self.driver.get(live_server.url)

        assert "open broadcast radio" == self.driver.title

        body = self.driver.find_element(By.TAG_NAME, "body").text
        # assert "2021-01-01T" in body

        # print(f'body: "{body}"')

        self.driver.save_screenshot("screenshots/start.png")

        self.driver.find_element(By.XPATH, "//a[normalize-space()='Login']").click()

        fill_form(
            self.driver,
            [
                ("//input[@name='email']", USER_DATA["email"]),
            ],
        )

        self.driver.find_element(
            By.XPATH, "//button[normalize-space()='Konto erstellen']"
        ).click()

        for entry in self.driver.get_log("browser"):
            print("// LOG", entry)

        time.sleep(2)

        print(mailoutbox)

        assert len(mailoutbox) == 1

        login_mail = mailoutbox[0]
        login_code = login_mail.subject.replace("Login Code: ", "")

        assert len(login_code) == 7

        self.driver.find_element(By.CSS_SELECTOR, ".token-input > input").send_keys(
            login_code
        )

        self.driver.find_element(
            By.XPATH, "//button[normalize-space()='Anmelden']"
        ).click()

        time.sleep(2)

        account_button = self.driver.find_element(By.CSS_SELECTOR, ".menu-toggle")
        # assert account_button.text == USER_DATA["email"][0].upper()
        assert account_button.text == ""

        self.driver.find_element(By.CSS_SELECTOR, ".menu-toggle").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//a[normalize-space()='Abmelden']").click()

        time.sleep(2)

        account_button = self.driver.find_element(By.CSS_SELECTOR, ".account-menu > a")
        assert account_button.text == "Login"

        # re-login with created account

        account_button.click()

        fill_form(
            self.driver,
            [
                ("//input[@name='email']", USER_DATA["email"]),
            ],
        )
        time.sleep(2)

        self.driver.find_element(
            By.XPATH, "//button[normalize-space()='Code senden']"
        ).click()
        time.sleep(2)

        assert len(mailoutbox) == 2

        login_mail = mailoutbox[1]
        login_code = login_mail.subject.replace("Login Code: ", "")

        assert len(login_code) == 7

        self.driver.find_element(By.CSS_SELECTOR, ".token-input > input").send_keys(
            login_code
        )

        self.driver.find_element(
            By.XPATH, "//button[normalize-space()='Anmelden']"
        ).click()

        time.sleep(2)

        # account_button = self.driver.find_element(By.CSS_SELECTOR, ".account-menu > a")
        account_button = self.driver.find_element(By.CSS_SELECTOR, ".menu-toggle")
        # assert account_button.text == USER_DATA["email"][0].upper()
        assert account_button.text == ""

        # for entry in self.driver.get_log("browser"):
        #     print("// LOG", entry)
