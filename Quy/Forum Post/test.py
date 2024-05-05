import json
import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class TestTeacherEditAssignmentsgrade(unittest.TestCase):
    def setup_method(self, method):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("--no-proxy-server")
        chrome_options.add_argument("--disable-gpu")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_cdp_cmd(
            "Network.setUserAgentOverride",
            {
                "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36"
            },
        )

        # try:
        #     file = open("data.json")
        #     self.vars = json.load(file)
        # except Exception:
        #     self.vars = {}

        self.driver.implicitly_wait(5)

        self.setup_authentication()

    def setup_authentication(self):
        self.driver.get("https://school.moodledemo.net/")
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.LINK_TEXT, "Log in"))
        )
        self.driver.find_element(By.LINK_TEXT, "Log in").click()

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable((By.ID, "username"))
        )
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("teacher")

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable((By.ID, "password"))
        )
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("moodle")

        self.driver.find_element(By.ID, "loginbtn").click()

    def teardown_method(self, method):
        self.driver.quit()

    def test_tC002001(self):
        self.driver.get("https://school.moodledemo.net/mod/assign/view.php?id=927")
        self.driver.set_window_size(1680, 1025)

        input = self.vars["tc002001"]["input"]

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable((By.LINK_TEXT, "Settings"))
        )
        self.driver.find_element(By.LINK_TEXT, "Settings").click()

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable((By.ID, "collapseElement-7"))
        )
        self.driver.find_element(By.ID, "collapseElement-7").click()

        grade_type_select = Select(
            self.driver.find_element(By.ID, "id_grade_modgrade_type")
        )
        grade_type_select.select_by_visible_text("Point")

        max_grade_input = self.driver.find_element(By.ID, "id_grade_modgrade_point")
        max_grade_input.click()
        max_grade_input.send_keys(Keys.HOME)
        max_grade_input.send_keys(Keys.SHIFT + Keys.END)
        max_grade_input.send_keys(input["max_grade"])

        passing_grade_input = self.driver.find_element(By.ID, "id_gradepass")
        passing_grade_input.click()
        passing_grade_input.send_keys(Keys.HOME)
        passing_grade_input.send_keys(Keys.SHIFT + Keys.END)
        passing_grade_input.send_keys(input["passing_grade"])

        self.driver.find_element(By.ID, "id_submitbutton").click()

        assert (
            self.driver.current_url
            == "https://school.moodledemo.net/mod/assign/view.php?id=927&forceview=1"
        )

    # def test_tC002002(self):
    #     self.driver.get("https://school.moodledemo.net/mod/assign/view.php?id=927")
    #     self.driver.set_window_size(1680, 1025)

    #     input = self.vars["tc002002"]["input"]

    #     WebDriverWait(self.driver, 5).until(
    #         expected_conditions.element_to_be_clickable((By.LINK_TEXT, "Settings"))
    #     )
    #     self.driver.find_element(By.LINK_TEXT, "Settings").click()

    #     WebDriverWait(self.driver, 5).until(
    #         expected_conditions.element_to_be_clickable((By.ID, "collapseElement-7"))
    #     )
    #     self.driver.find_element(By.ID, "collapseElement-7").click()

    #     grade_type_select = Select(
    #         self.driver.find_element(By.ID, "id_grade_modgrade_type")
    #     )
    #     grade_type_select.select_by_visible_text("Point")

    #     max_grade_input = self.driver.find_element(By.ID, "id_grade_modgrade_point")
    #     max_grade_input.click()
    #     max_grade_input.send_keys(Keys.HOME)
    #     max_grade_input.send_keys(Keys.SHIFT + Keys.END)
    #     max_grade_input.send_keys(input["max_grade"])

    #     passing_grade_input = self.driver.find_element(By.ID, "id_gradepass")
    #     passing_grade_input.click()
    #     passing_grade_input.send_keys(Keys.HOME)
    #     passing_grade_input.send_keys(Keys.SHIFT + Keys.END)
    #     passing_grade_input.send_keys(input["passing_grade"])

    #     self.driver.find_element(By.ID, "id_submitbutton").click()

    #     assert (
    #         self.driver.current_url
    #         == "https://school.moodledemo.net/mod/assign/view.php?id=927&forceview=1"
    #     )

    # def test_tC002003(self):
    #     self.driver.get("https://school.moodledemo.net/mod/assign/view.php?id=927")
    #     self.driver.set_window_size(1680, 1025)

    #     input = self.vars["tc002003"]["input"]

    #     WebDriverWait(self.driver, 5).until(
    #         expected_conditions.element_to_be_clickable((By.LINK_TEXT, "Settings"))
    #     )
    #     self.driver.find_element(By.LINK_TEXT, "Settings").click()

    #     WebDriverWait(self.driver, 5).until(
    #         expected_conditions.element_to_be_clickable((By.ID, "collapseElement-7"))
    #     )
    #     self.driver.find_element(By.ID, "collapseElement-7").click()

    #     grade_type_select = Select(
    #         self.driver.find_element(By.ID, "id_grade_modgrade_type")
    #     )
    #     grade_type_select.select_by_visible_text("Point")

    #     max_grade_input = self.driver.find_element(By.ID, "id_grade_modgrade_point")
    #     max_grade_input.click()
    #     max_grade_input.send_keys(Keys.HOME)
    #     max_grade_input.send_keys(Keys.SHIFT + Keys.END)
    #     max_grade_input.send_keys(input["max_grade"])

    #     passing_grade_input = self.driver.find_element(By.ID, "id_gradepass")
    #     passing_grade_input.click()
    #     passing_grade_input.send_keys(Keys.HOME)
    #     passing_grade_input.send_keys(Keys.SHIFT + Keys.END)
    #     passing_grade_input.send_keys(input["passing_grade"])

    #     self.driver.find_element(By.ID, "id_submitbutton").click()

    #     assert (
    #         self.driver.current_url
    #         == "https://school.moodledemo.net/mod/assign/view.php?id=927&forceview=1"
    #     )


if __name__ == "__main__":
    unittest.main()
