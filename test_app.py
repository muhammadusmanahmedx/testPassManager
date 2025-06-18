import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

class NextAppTests(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.url = "http://3.88.195.52:5100"  # 🔁 Replace with actual EC2 IP

    def tearDown(self):
        self.driver.quit()

    def test_homepage_title(self):
        self.driver.get(self.url)
        self.assertIn("Home", self.driver.title)

    def test_navbar_present(self):
        self.driver.get(self.url)
        navbar = self.driver.find_element(By.TAG_NAME, "nav")
        self.assertIsNotNone(navbar)

    def test_login_page_loads(self):
        self.driver.get(f"{self.url}/login")
        self.assertIn("Login", self.driver.page_source)

    def test_invalid_login(self):
        self.driver.get(f"{self.url}/login")
        self.driver.find_element(By.NAME, "email").send_keys("fake@example.com")
        self.driver.find_element(By.NAME, "password").send_keys("wrongpass")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)
        self.assertIn("Invalid", self.driver.page_source)

    def test_signup_page_loads(self):
        self.driver.get(f"{self.url}/signup")
        self.assertIn("Sign Up", self.driver.page_source)

    def test_form_submission(self):
        self.driver.get(f"{self.url}/contact")
        self.driver.find_element(By.NAME, "name").send_keys("Ali")
        self.driver.find_element(By.NAME, "email").send_keys("ali@example.com")
        self.driver.find_element(By.NAME, "message").send_keys("Test message")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)
        self.assertIn("Thank you", self.driver.page_source)

    def test_login_success_redirect(self):
        self.driver.get(f"{self.url}/login")
        self.driver.find_element(By.NAME, "email").send_keys("test@example.com")
        self.driver.find_element(By.NAME, "password").send_keys("123456")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)
        self.assertIn("Dashboard", self.driver.page_source)

    def test_dashboard_requires_login(self):
        self.driver.get(f"{self.url}/dashboard")
        self.assertTrue("/login" in self.driver.current_url or "Unauthorized" in self.driver.page_source)

    def test_search_functionality(self):
        self.driver.get(self.url)
        search = self.driver.find_element(By.NAME, "search")
        search.send_keys("Test Item")
        search.submit()
        time.sleep(1)
        self.assertIn("Test Item", self.driver.page_source)

    def test_footer_present(self):
        self.driver.get(self.url)
        footer = self.driver.find_element(By.TAG_NAME, "footer")
        self.assertIsNotNone(footer)

if __name__ == "__main__":
    unittest.main()
