import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class TestYandexAuthorization(unittest.TestCase):

    def setUp(self) -> None:
        self.driver = webdriver.Firefox()

    def test_authorize_in_yandex(self):
        driver = self.driver
        driver.get(r"https://passport.yandex.ru/auth/list")
        element = driver.find_element(by=By.ID, value="passp-field-login")
        # Enter login.
        element.send_keys("")
        driver.find_element(by=By.ID, value="passp:sign-in").click()
        element = driver.find_element(by=By.ID, value="passp-field-passwd")
        # Enter password.
        element.send_keys("")
        driver.find_element(by=By.ID, value="passp:sign-in").click()
        try:
            element = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, "personal-info__first"))
            )
        except TimeoutException:
            pass
        username = driver.find_element(by=By.CLASS_NAME, value="personal-info__first")
        user_lastname = driver.find_element(by=By.CLASS_NAME, value="personal-info__last")
        self.assertTrue(username and user_lastname)

    def tearDown(self) -> None:
        self.driver.close()


if __name__ == '__main__':
    unittest.main()