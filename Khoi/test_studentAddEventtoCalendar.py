import json
import time
import unittest

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class TestStudentAddEventtoCalendar(unittest.TestCase):
    def __get_seconds_since_epoch(self, given_date):
        return int(
            time.mktime(time.strptime(given_date, "%d-%m-%Y"))
            - time.mktime(time.gmtime(0))
        )

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

        try:
            file = open("data.json")
            self.vars = json.load(file)
        except Exception:
            self.vars = {}

        self.__months = {
            "1": "January",
            "2": "February",
            "3": "March",
            "4": "April",
            "5": "May",
            "6": "June",
            "7": "July",
            "8": "August",
            "9": "September",
            "10": "October",
            "11": "November",
            "12": "December",
        }

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
        self.driver.find_element(By.ID, "username").send_keys("student")

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable((By.ID, "password"))
        )
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("moodle")

        self.driver.find_element(By.ID, "loginbtn").click()

    def teardown_method(self, method):
        self.driver.quit()

    def test_tC001001(self):
        self.driver.get("https://school.moodledemo.net/calendar/view.php?view=month")
        self.driver.set_window_size(1680, 1025)

        input = self.vars["tc001001"]["input"]

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='new-event-button']")
            )
        )
        self.driver.find_element(
            By.XPATH, "//button[@data-action='new-event-button']"
        ).click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            )
        )

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable((By.ID, "id_name"))
        )
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(input["event_name"])

        day, month, year = input["date"].split("-")

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable((By.ID, "id_timestart_day"))
        )
        day_select = Select(self.driver.find_element(By.ID, "id_timestart_day"))
        day_select.select_by_value(day)

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable((By.ID, "id_timestart_month"))
        )
        month_select = Select(self.driver.find_element(By.ID, "id_timestart_month"))
        month_select.select_by_value(month)

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable((By.ID, "id_timestart_year"))
        )
        year_select = Select(self.driver.find_element(By.ID, "id_timestart_year"))
        year_select.select_by_visible_text(year)

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='save']")
            )
        )
        self.driver.find_element(By.XPATH, "//button[@data-action='save']").click()

        WebDriverWait(self.driver, 5).until(
            expected_conditions.invisibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            )
        )

        time_input = self.__get_seconds_since_epoch(input["date"])

        is_success = False
        for _ in range(3):
            if is_success is True:
                break
            try:
                self.driver.get(
                    f"https://school.moodledemo.net/calendar/view.php?view=month&time={time_input}"
                )
                WebDriverWait(self.driver, 5).until(
                    expected_conditions.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, "h2[class='current']"),
                        f"{self.__months[month]} {year}",
                    )
                )
                is_success = True
            except:
                self.driver.refresh()
        if is_success is False:
            raise TimeoutException()

        elements = self.driver.find_elements(
            By.XPATH,
            f"//td[@data-day='{day}']/div/div[@data-region='day-content']/ul/li/a[@title='{input['event_name']}']",
        )
        assert len(elements) > 0

    def test_tC001002(self):
        self.driver.get("https://school.moodledemo.net/calendar/view.php?view=month")
        self.driver.set_window_size(1680, 1025)

        input = self.vars["tc001002"]["input"]

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='new-event-button']")
            )
        )
        self.driver.find_element(
            By.XPATH, "//button[@data-action='new-event-button']"
        ).click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            )
        )
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(input["event_name"])

        day, month, year = input["date"].split("-")
        day_select = Select(self.driver.find_element(By.ID, "id_timestart_day"))
        day_select.select_by_visible_text(day)
        month_select = Select(self.driver.find_element(By.ID, "id_timestart_month"))
        month_select.select_by_value(month)
        year_select = Select(self.driver.find_element(By.ID, "id_timestart_year"))
        year_select.select_by_visible_text(year)
        self.driver.find_element(By.LINK_TEXT, "Show more...").click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable((By.ID, "id_location"))
        )
        self.driver.find_element(By.ID, "id_location").click()
        self.driver.find_element(By.ID, "id_location").send_keys(input["location"])
        self.driver.find_element(
            By.CSS_SELECTOR, ".form-check-inline:nth-child(1)"
        ).click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='save']")
            )
        )
        self.driver.find_element(By.XPATH, "//button[@data-action='save']").click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.invisibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            )
        )

        time_input = self.__get_seconds_since_epoch(input["date"])

        is_success = False
        for _ in range(3):
            if is_success is True:
                break
            try:
                self.driver.get(
                    f"https://school.moodledemo.net/calendar/view.php?view=month&time={time_input}"
                )
                WebDriverWait(self.driver, 5).until(
                    expected_conditions.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, "h2[class='current']"),
                        f"{self.__months[month]} {year}",
                    )
                )
                is_success = True
            except:
                self.driver.refresh()
        if is_success is False:
            raise TimeoutException()

        elements = self.driver.find_elements(
            By.XPATH,
            f"//td[@data-day='{day}']/div/div[@data-region='day-content']/ul/li/a[@title='{input['event_name']}']",
        )
        assert len(elements) > 0

    def test_tC001003(self):
        self.driver.get("https://school.moodledemo.net/calendar/view.php?view=month")
        self.driver.set_window_size(1680, 1025)

        input = self.vars["tc001003"]["input"]
        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='new-event-button']")
            )
        )
        self.driver.find_element(
            By.XPATH, "//button[@data-action='new-event-button']"
        ).click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            )
        )
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(input["event_name"])

        day, month, year = input["date"].split("-")
        day_select = Select(self.driver.find_element(By.ID, "id_timestart_day"))
        day_select.select_by_visible_text(day)
        month_select = Select(self.driver.find_element(By.ID, "id_timestart_month"))
        month_select.select_by_value(month)
        year_select = Select(self.driver.find_element(By.ID, "id_timestart_year"))
        year_select.select_by_visible_text(year)
        self.driver.find_element(By.LINK_TEXT, "Show more...").click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable((By.ID, "id_location"))
        )
        self.driver.find_element(By.ID, "id_location").click()
        self.driver.find_element(By.ID, "id_location").send_keys(input["location"])
        self.driver.find_element(
            By.CSS_SELECTOR, ".form-check-inline:nth-child(1)"
        ).click()
        self.driver.find_element(By.ID, "id_repeat").click()
        self.driver.find_element(By.ID, "id_repeats").click()
        self.driver.find_element(By.ID, "id_repeats").send_keys(input["repeat"])
        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='save']")
            )
        )
        self.driver.find_element(By.XPATH, "//button[@data-action='save']").click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.invisibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            )
        )

        for i in range(int(input["repeat"])):
            time_input = (
                self.__get_seconds_since_epoch(input["date"]) + i * 7 * 24 * 60 * 60
            )
            curr_date = time.gmtime(time_input)
            curr_day, curr_month, curr_year = (
                str(curr_date.tm_mday),
                str(curr_date.tm_mon),
                str(curr_date.tm_year),
            )

            is_success = False
            for _ in range(3):
                if is_success is True:
                    break
                try:
                    self.driver.get(
                        f"https://school.moodledemo.net/calendar/view.php?view=month&time={time_input}"
                    )
                    WebDriverWait(self.driver, 5).until(
                        expected_conditions.text_to_be_present_in_element(
                            (By.CSS_SELECTOR, "h2[class='current']"),
                            f"{self.__months[month]} {year}",
                        )
                    )
                    is_success = True
                except:
                    self.driver.refresh()
            if is_success is False:
                raise TimeoutException()

            elements = self.driver.find_elements(
                By.XPATH,
                f"//td[@data-day='{curr_day}']/div/div[@data-region='day-content']/ul/li/a[@title='{input['event_name']}']",
            )
            assert len(elements) > 0

    def test_tC001004(self):
        self.driver.get("https://school.moodledemo.net/calendar/view.php?view=month")
        self.driver.set_window_size(1680, 1025)

        input = self.vars["tc001004"]["input"]
        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='new-event-button']")
            )
        )
        self.driver.find_element(
            By.XPATH, "//button[@data-action='new-event-button']"
        ).click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            )
        )
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(input["event_name"])

        day, month, year = input["date"].split("-")
        day_select = Select(self.driver.find_element(By.ID, "id_timestart_day"))
        day_select.select_by_visible_text(day)
        month_select = Select(self.driver.find_element(By.ID, "id_timestart_month"))
        month_select.select_by_value(month)
        year_select = Select(self.driver.find_element(By.ID, "id_timestart_year"))
        year_select.select_by_visible_text(year)
        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='save']")
            )
        )
        self.driver.find_element(By.XPATH, "//button[@data-action='save']").click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.invisibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            )
        )

        time_input = self.__get_seconds_since_epoch(input["date"])

        is_success = False
        for _ in range(3):
            if is_success is True:
                break
            try:
                self.driver.get(
                    f"https://school.moodledemo.net/calendar/view.php?view=month&time={time_input}"
                )
                WebDriverWait(self.driver, 5).until(
                    expected_conditions.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, "h2[class='current']"),
                        f"{self.__months[month]} {year}",
                    )
                )
                is_success = True
            except:
                self.driver.refresh()
        if is_success is False:
            raise TimeoutException()

        elements = self.driver.find_elements(
            By.XPATH,
            f"//td[@data-day='{day}']/div/div[@data-region='day-content']/ul/li/a[@title='{input['event_name']}']",
        )
        assert len(elements) > 0

    def test_tC001005(self):
        self.driver.get("https://school.moodledemo.net/calendar/view.php?view=month")
        self.driver.set_window_size(1680, 1025)

        input = self.vars["tc001005"]["input"]
        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='new-event-button']")
            )
        )
        self.driver.find_element(
            By.XPATH, "//button[@data-action='new-event-button']"
        ).click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            )
        )
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(input["event_name"])

        day, month, year = input["date"].split("-")
        day_select = Select(self.driver.find_element(By.ID, "id_timestart_day"))
        day_select.select_by_visible_text(day)
        month_select = Select(self.driver.find_element(By.ID, "id_timestart_month"))
        month_select.select_by_value(month)
        year_select = Select(self.driver.find_element(By.ID, "id_timestart_year"))
        year_select.select_by_visible_text(year)
        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='save']")
            )
        )
        self.driver.find_element(By.XPATH, "//button[@data-action='save']").click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.invisibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            )
        )
        time_input = self.__get_seconds_since_epoch(
            self.vars["tc001005"]["expected"]["date"]
        )

        expected_day, expected_month, expected_year = self.vars["tc001005"]["expected"][
            "date"
        ].split("-")

        is_success = False
        for _ in range(3):
            if is_success is True:
                break
            try:
                self.driver.get(
                    f"https://school.moodledemo.net/calendar/view.php?view=month&time={time_input}"
                )
                WebDriverWait(self.driver, 5).until(
                    expected_conditions.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, "h2[class='current']"),
                        f"{self.__months[expected_month]} {expected_year}",
                    )
                )
                is_success = True
            except:
                self.driver.refresh()
        if is_success is False:
            raise TimeoutException()

        elements = self.driver.find_elements(
            By.XPATH,
            f"//td[@data-day='{expected_day}']/div/div[@data-region='day-content']/ul/li/a[@title='{input['event_name']}']",
        )
        assert len(elements) > 0

    def test_tC001006(self):
        self.driver.get("https://school.moodledemo.net/calendar/view.php?view=month")
        self.driver.set_window_size(1680, 1025)

        input = self.vars["tc001006"]["input"]
        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='new-event-button']")
            )
        )
        self.driver.find_element(
            By.XPATH, "//button[@data-action='new-event-button']"
        ).click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            )
        )
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(input["event_name"])

        day, month, year = input["date"].split("-")
        day_select = Select(self.driver.find_element(By.ID, "id_timestart_day"))
        day_select.select_by_visible_text(day)
        month_select = Select(self.driver.find_element(By.ID, "id_timestart_month"))
        month_select.select_by_value(month)
        year_select = Select(self.driver.find_element(By.ID, "id_timestart_year"))
        year_select.select_by_visible_text(year)
        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='save']")
            )
        )
        self.driver.find_element(By.XPATH, "//button[@data-action='save']").click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.invisibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            )
        )

        time_input = self.__get_seconds_since_epoch(
            self.vars["tc001006"]["expected"]["date"]
        )

        expected_day, expected_month, expected_year = self.vars["tc001006"]["expected"][
            "date"
        ].split("-")

        is_success = False
        for _ in range(3):
            if is_success is True:
                break
            try:
                self.driver.get(
                    f"https://school.moodledemo.net/calendar/view.php?view=month&time={time_input}"
                )
                WebDriverWait(self.driver, 5).until(
                    expected_conditions.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, "h2[class='current']"),
                        f"{self.__months[expected_month]} {expected_year}",
                    )
                )
                is_success = True
            except:
                self.driver.refresh()
        if is_success is False:
            raise TimeoutException()

        elements = self.driver.find_elements(
            By.XPATH,
            f"//td[@data-day='{expected_day}']/div/div[@data-region='day-content']/ul/li/a[@title='{input['event_name']}']",
        )
        assert len(elements) > 0

    def test_tC001007(self):
        self.driver.get("https://school.moodledemo.net/calendar/view.php?view=month")
        self.driver.set_window_size(1680, 1025)

        input = self.vars["tc001007"]["input"]
        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='new-event-button']")
            )
        )
        self.driver.find_element(
            By.XPATH, "//button[@data-action='new-event-button']"
        ).click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            )
        )
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(input["event_name"])

        day, month, year = input["date"].split("-")
        day_select = Select(self.driver.find_element(By.ID, "id_timestart_day"))
        day_select.select_by_visible_text(day)
        month_select = Select(self.driver.find_element(By.ID, "id_timestart_month"))
        month_select.select_by_value(month)
        year_select = Select(self.driver.find_element(By.ID, "id_timestart_year"))
        year_select.select_by_visible_text(year)
        self.driver.find_element(By.LINK_TEXT, "Show more...").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".form-check-inline:nth-child(1)"
        ).click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='save']")
            )
        )
        self.driver.find_element(By.XPATH, "//button[@data-action='save']").click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.invisibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            )
        )

        time_input = self.__get_seconds_since_epoch(input["date"])

        is_success = False
        for _ in range(3):
            if is_success is True:
                break
            try:
                self.driver.get(
                    f"https://school.moodledemo.net/calendar/view.php?view=month&time={time_input}"
                )
                WebDriverWait(self.driver, 5).until(
                    expected_conditions.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, "h2[class='current']"),
                        f"{self.__months[month]} {year}",
                    )
                )
                is_success = True
            except:
                self.driver.refresh()
        if is_success is False:
            raise TimeoutException()

        elements = self.driver.find_elements(
            By.XPATH,
            f"//td[@data-day='{day}']/div/div[@data-region='day-content']/ul/li/a[@title='{input['event_name']}']",
        )
        assert len(elements) > 0

    def test_tC001008(self):
        self.driver.get("https://school.moodledemo.net/calendar/view.php?view=month")
        self.driver.set_window_size(1680, 1025)

        input = self.vars["tc001008"]["input"]

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='new-event-button']")
            )
        )
        self.driver.find_element(
            By.XPATH, "//button[@data-action='new-event-button']"
        ).click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            )
        )
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(input["event_name"])

        day, month, year = input["date"].split("-")
        day_select = Select(self.driver.find_element(By.ID, "id_timestart_day"))
        day_select.select_by_visible_text(day)

        month_select = Select(self.driver.find_element(By.ID, "id_timestart_month"))
        month_select.select_by_value(month)

        year_select = Select(self.driver.find_element(By.ID, "id_timestart_year"))
        year_select.select_by_visible_text(year)

        self.driver.find_element(By.LINK_TEXT, "Show more...").click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable((By.ID, "id_duration_1"))
        )
        self.driver.find_element(By.ID, "id_duration_1").click()

        until_day, until_month, until_year = input["until"].split("-")
        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.ID, "id_timedurationuntil_day")
            )
        )
        until_day_select = Select(
            self.driver.find_element(By.ID, "id_timedurationuntil_day")
        )
        until_day_select.select_by_visible_text(until_day)

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.ID, "id_timedurationuntil_month")
            )
        )
        until_month_select = Select(
            self.driver.find_element(By.ID, "id_timedurationuntil_month")
        )
        until_month_select.select_by_value(until_month)

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.ID, "id_timedurationuntil_year")
            )
        )
        until_year_select = Select(
            self.driver.find_element(By.ID, "id_timedurationuntil_year")
        )
        until_year_select.select_by_visible_text(until_year)

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='save']")
            )
        )
        self.driver.find_element(By.XPATH, "//button[@data-action='save']").click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.invisibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            )
        )

        time_input = self.__get_seconds_since_epoch(input["date"])

        is_success = False
        for _ in range(3):
            if is_success is True:
                break
            try:
                self.driver.get(
                    f"https://school.moodledemo.net/calendar/view.php?view=month&time={time_input}"
                )
                WebDriverWait(self.driver, 5).until(
                    expected_conditions.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, "h2[class='current']"),
                        f"{self.__months[month]} {year}",
                    )
                )
                is_success = True
            except:
                self.driver.refresh()
        if is_success is False:
            raise TimeoutException()

        elements = self.driver.find_elements(
            By.XPATH,
            f"//td[@data-day]/div/div[@data-region='day-content']/ul/li/a[@title='{input['event_name']}']",
        )
        assert len(elements) % (int(until_day) - int(day) + 1) == 0

    def test_tC001009(self):
        self.driver.get("https://school.moodledemo.net/calendar/view.php?view=month")
        self.driver.set_window_size(1680, 1025)

        input = self.vars["tc001009"]["input"]
        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='new-event-button']")
            )
        )
        self.driver.find_element(
            By.XPATH, "//button[@data-action='new-event-button']"
        ).click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            )
        )

        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(input["event_name"])

        day, month, year = input["date"].split("-")
        day_select = Select(self.driver.find_element(By.ID, "id_timestart_day"))
        day_select.select_by_visible_text(day)

        month_select = Select(self.driver.find_element(By.ID, "id_timestart_month"))
        month_select.select_by_value(month)

        year_select = Select(self.driver.find_element(By.ID, "id_timestart_year"))
        year_select.select_by_visible_text(year)

        self.driver.find_element(By.LINK_TEXT, "Show more...").click()

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable((By.ID, "id_duration_1"))
        )
        self.driver.find_element(By.ID, "id_duration_1").click()
        self.driver.find_element(By.ID, "id_timedurationuntil_day").click()

        until_day, until_month, until_year = input["until"].split("-")
        until_day_select = Select(
            self.driver.find_element(By.ID, "id_timedurationuntil_day")
        )
        until_day_select.select_by_visible_text(until_day)

        until_month_select = Select(
            self.driver.find_element(By.ID, "id_timedurationuntil_month")
        )
        until_month_select.select_by_value(until_month)

        until_year_select = Select(
            self.driver.find_element(By.ID, "id_timedurationuntil_year")
        )
        until_year_select.select_by_visible_text(until_year)

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='save']")
            )
        )
        self.driver.find_element(By.XPATH, "//button[@data-action='save']").click()

        WebDriverWait(self.driver, 20).until(
            expected_conditions.text_to_be_present_in_element(
                (By.ID, "fgroup_id_error_durationgroup"),
                self.vars["tc001009"]["expected"]["error"],
            )
        )

    def test_tC001010(self):
        self.driver.get("https://school.moodledemo.net/calendar/view.php?view=month")
        self.driver.set_window_size(1680, 1025)

        input = self.vars["tc001010"]["input"]

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='new-event-button']")
            )
        )
        self.driver.find_element(
            By.XPATH, "//button[@data-action='new-event-button']"
        ).click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            )
        )

        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(input["event_name"])

        day, month, year = input["date"].split("-")
        day_select = Select(self.driver.find_element(By.ID, "id_timestart_day"))
        day_select.select_by_visible_text(day)

        month_select = Select(self.driver.find_element(By.ID, "id_timestart_month"))
        month_select.select_by_value(month)

        year_select = Select(self.driver.find_element(By.ID, "id_timestart_year"))
        year_select.select_by_visible_text(year)

        self.driver.find_element(By.LINK_TEXT, "Show more...").click()

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable((By.ID, "id_duration_2"))
        )
        self.driver.find_element(By.ID, "id_duration_2").click()
        self.driver.find_element(By.ID, "id_timedurationminutes").click()
        self.driver.find_element(By.ID, "id_timedurationminutes").send_keys(
            input["duration"]
        )

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='save']")
            )
        )
        self.driver.find_element(By.XPATH, "//button[@data-action='save']").click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.invisibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            )
        )

        time_input = self.__get_seconds_since_epoch(input["date"])

        is_success = False
        for _ in range(3):
            if is_success is True:
                break
            try:
                self.driver.get(
                    f"https://school.moodledemo.net/calendar/view.php?view=month&time={time_input}"
                )
                WebDriverWait(self.driver, 5).until(
                    expected_conditions.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, "h2[class='current']"),
                        f"{self.__months[month]} {year}",
                    )
                )
                is_success = True
            except:
                self.driver.refresh()
        if is_success is False:
            raise TimeoutException()

        elements = self.driver.find_elements(
            By.XPATH,
            f"//td[@data-day='{day}']/div/div[@data-region='day-content']/ul/li/a[@title='{input['event_name']}']",
        )
        assert len(elements) > 0

    def test_tC001011(self):
        self.driver.get("https://school.moodledemo.net/calendar/view.php?view=month")
        self.driver.set_window_size(1680, 1025)

        input = self.vars["tc001011"]["input"]

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='new-event-button']")
            )
        )
        self.driver.find_element(
            By.XPATH, "//button[@data-action='new-event-button']"
        ).click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            )
        )
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(input["event_name"])

        day, month, year = input["date"].split("-")
        day_select = Select(self.driver.find_element(By.ID, "id_timestart_day"))
        day_select.select_by_visible_text(day)

        month_select = Select(self.driver.find_element(By.ID, "id_timestart_month"))
        month_select.select_by_value(month)

        year_select = Select(self.driver.find_element(By.ID, "id_timestart_year"))
        year_select.select_by_visible_text(year)

        self.driver.find_element(By.LINK_TEXT, "Show more...").click()

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable((By.ID, "id_duration_2"))
        )
        self.driver.find_element(By.ID, "id_duration_2").click()
        self.driver.find_element(By.ID, "id_timedurationminutes").click()
        self.driver.find_element(By.ID, "id_timedurationminutes").send_keys(
            input["duration"]
        )

        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//button[@data-action='save']")
            )
        )
        self.driver.find_element(By.XPATH, "//button[@data-action='save']").click()

        WebDriverWait(self.driver, 20).until(
            expected_conditions.text_to_be_present_in_element(
                (By.ID, "fgroup_id_error_durationgroup"),
                self.vars["tc001011"]["expected"]["error"],
            )
        )
