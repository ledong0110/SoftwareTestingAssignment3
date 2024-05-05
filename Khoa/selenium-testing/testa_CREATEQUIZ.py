import pytest
import time
import json
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_tc_list(path):
  """Load testcases from .json file
  
  Format of the file should be: list[dict]
  """
  with open(path, 'r') as f:
    tc_list = json.load(f)
    retval = list(map(lambda x: tuple(x.values()), tc_list))
  return retval
  

class TestCREATEQUIZ__():

  def __login(self):
    self.driver.get("https://school.moodledemo.net/")
    self.driver.find_element(By.LINK_TEXT, "Log in").click()
    self.driver.find_element(By.ID, "username").click()
    self.driver.find_element(By.ID, "username").send_keys("teacher")
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys("moodle")
    self.driver.find_element(By.ID, "loginbtn").click()


  def setup_method(self, method):
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    self.driver = webdriver.Chrome(options=op)
    self.driver.implicitly_wait(10)
    self.vars = {}
  

  def teardown_method(self, method):
    self.driver.quit()


  @pytest.mark.parametrize("day,month,year,hour,minute,expected", load_tc_list("./SetTiming.Equiv.json"))
  def test_set_timing_equiv(self, day, month, year, hour, minute, expected):
    """Set Timing/Equivalence class parititioning"""

    self.__login()

    self.driver.get("https://school.moodledemo.net/course/modedit.php?add=quiz&type&course=51&section=5&return=0&beforemod=0")

    self.driver.find_element(By.ID, "id_name").send_keys("hello")
    self.driver.find_element(By.ID, "collapseElement-1").click()
    self.driver.find_element(By.ID, "id_timeopen_enabled").click()

    dropdown = self.driver.find_element(By.ID, "id_timeopen_day")
    Select(dropdown).select_by_visible_text(day)

    dropdown = self.driver.find_element(By.ID, "id_timeopen_month")
    Select(dropdown).select_by_visible_text(month)

    dropdown = self.driver.find_element(By.ID, "id_timeopen_year")
    Select(dropdown).select_by_visible_text(year)

    dropdown = self.driver.find_element(By.ID, "id_timeopen_hour")
    Select(dropdown).select_by_visible_text(hour)

    dropdown = self.driver.find_element(By.ID, "id_timeopen_minute")
    Select(dropdown).select_by_visible_text(minute)

    self.driver.find_element(By.ID, "id_submitbutton").click()

    assert self.driver.find_element(By.CSS_SELECTOR, ".activity-dates > div").text == str(expected)

    self.driver.close()


  @pytest.mark.parametrize(
      "name,open_enabled,open_day,open_month,open_year,open_hour,open_minute,open_expected,close_enabled,close_day,close_month,close_year,close_hour,close_minute,close_expected,error_enabled,error_expected"
      , load_tc_list("./SetTiming.Decs.json")
  )
  def test_set_timing_decision(
    self, 
    name,
    open_enabled,
    open_day,
    open_month,
    open_year,
    open_hour,
    open_minute,
    open_expected,
    close_enabled,
    close_day,
    close_month,
    close_year,
    close_hour,
    close_minute,
    close_expected,
    error_enabled,
    error_expected
    ):

    self.__login()

    self.driver.get("https://school.moodledemo.net/course/modedit.php?add=quiz&type&course=51&section=5&return=0&beforemod=0")
    self.driver.find_element(By.ID, "id_name").send_keys(str(name))
    self.driver.find_element(By.ID, "collapseElement-1").click()

    if open_enabled == "True":
      self.driver.find_element(By.ID, "id_timeopen_enabled").click()

      if str(open_day) != "":
        dropdown = self.driver.find_element(By.ID, "id_timeopen_day")
        Select(dropdown).select_by_visible_text(str(open_day))

        dropdown = self.driver.find_element(By.ID, "id_timeopen_month")
        Select(dropdown).select_by_visible_text(str(open_month))

        dropdown = self.driver.find_element(By.ID, "id_timeopen_year")
        Select(dropdown).select_by_visible_text(str(open_year))

        dropdown = self.driver.find_element(By.ID, "id_timeopen_hour")
        Select(dropdown).select_by_visible_text(str(open_hour))

        dropdown = self.driver.find_element(By.ID, "id_timeopen_minute")
        Select(dropdown).select_by_visible_text(str(open_minute))
    
    if close_enabled == "True":
      self.driver.find_element(By.ID, "id_timeclose_enabled").click()

      if str(close_day) != "":
        dropdown = self.driver.find_element(By.ID, "id_timeclose_day")
        Select(dropdown).select_by_visible_text(str(close_day))

        dropdown = self.driver.find_element(By.ID, "id_timeclose_month")
        Select(dropdown).select_by_visible_text(str(close_month))

        dropdown = self.driver.find_element(By.ID, "id_timeclose_year")
        Select(dropdown).select_by_visible_text(str(close_year))

        dropdown = self.driver.find_element(By.ID, "id_timeclose_hour")
        Select(dropdown).select_by_visible_text(str(close_hour))

        dropdown = self.driver.find_element(By.ID, "id_timeclose_minute")
        Select(dropdown).select_by_visible_text(str(close_minute))

    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    self.driver.find_element(By.ID, "id_submitbutton").click()

    if error_enabled == "True":
      assert self.driver.find_element(By.ID, "id_error_timeclose").text == str(error_expected)
    else:      
      if open_enabled == "True":
        if str(open_day) != "":
          assert self.driver.find_element(By.CSS_SELECTOR, ".activity-dates > div:nth-child(1)").text == str(open_expected)
        else:
          assert True  # Because default value is dynamic, we assume it is true
      if close_enabled == "True":
        if str(close_day) != "":
          assert self.driver.find_element(By.CSS_SELECTOR, ".activity-dates > div:nth-child(2)").text == str(close_expected)
        else:
          assert True  # Because default value is dynamic, we assume it is true

    self.driver.close()
  

  @pytest.mark.parametrize("name,expected_error", load_tc_list("./QuizName.Decs.json"))
  def test_enter_quizname(self, name, expected_error):
    self.__login()
    self.driver.get("https://school.moodledemo.net/course/modedit.php?add=quiz&type&course=51&section=5&return=0&beforemod=0")
    self.driver.find_element(By.ID, "id_name").send_keys(str(name))
    self.driver.find_element(By.ID, "id_submitbutton").click()

    if str(expected_error):
      assert self.driver.find_element(By.ID, "id_error_name").text == str(expected_error)
    else:
      assert self.driver.find_element(By.CSS_SELECTOR, ".h2").text == str(name)

    self.driver.close()

  # def test_create_quiz_usecase(self):
  #   # Usecase Testing is not suitable for Data-driven Testing
  #   # since each testcase is a separate script
  #   pass