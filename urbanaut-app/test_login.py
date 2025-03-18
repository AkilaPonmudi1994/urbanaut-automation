import time
from unittest import skip

import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import random

class TestUrbanaut:
    # Constants
    BASE_URL = "https://urbanaut.app/"

    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, request):
        print('*********setting up******')
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        cls = request.cls
        driver.get(cls.BASE_URL)
        driver.maximize_window()
        driver.implicitly_wait(3)
        cls.driver = driver
        cls.wait = WebDriverWait(cls.driver, 10)
        yield
        # teardown
        print('*****teardown*****')
        cls.driver.quit()

    def test_signup(self):
        """Signup to the application
        """
        self.driver.find_element(By.ID, "Login").click()
        self.driver.find_element(By.ID, "sign-up").click()
        self.driver.find_element(By.ID, "signup-name").send_keys("Akila")
        self.driver.find_element(By.ID, "signup-email").send_keys("akilap15@gmail.com")
        self.driver.find_element(By.ID, "signup-city").send_keys("Coimbatore")
        self.driver.find_element(By.NAME, "password").send_keys("Akila@123")
        self.driver.find_element(By.NAME, "repassword").send_keys("Akila@123")
        time.sleep(2)
        self.driver.find_element(By.ID, "sign-up").click()
        assert self.driver.title=="Travel better with Urbanaut"
        print("Logged in to the urbanaut application successfully")
        self.driver.implicitly_wait(5)
        #Testing logout after signup
        profile_element = self.driver.find_element(By.ID, "profile_pic")
        profile_element.click()
        assert  profile_element.is_displayed()
        self.driver.find_element(By.ID, "logout").click()
        time.sleep(2)

    def test_login_success(self):
        """Login to the application
        """
        self.driver.find_element(By.ID, "Login").click()
        self.driver.find_element(By.ID, "login-email").send_keys("akilap13@urbanaut.com")
        self.driver.find_element(By.ID, "login-password").send_keys("Akila@123")
        self.driver.find_element(By.ID, "login").click()
        # Wait up to 10 seconds for the profile picture element to be visible
        profile_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "profile_pic"))
        )
        assert profile_element.is_displayed()
        profile_element.click()
        self.driver.find_element(By.ID, "logout").click()
        time.sleep(3)

    def test_login_failure(self):
        """Login to the application with incorrect credentials
        """
        self.driver.find_element(By.ID, "Login").click()
        self.driver.find_element(By.ID, "login-email").send_keys("akilap1@urbanaut.com")
        self.driver.find_element(By.ID, "login-password").send_keys("akila@123")
        self.driver.find_element(By.ID, "login").click()
        # Wait for the error message to be visible
        error_message_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='mb-2 text-danger']"))
        )
        # Extract the error message text
        error_message_text = error_message_element.text
        print(f"Captured error message: {error_message_text}")
        # Define the expected error message
        expected_error_message = "Unable to log in with provided credentials."
        assert error_message_text == expected_error_message
