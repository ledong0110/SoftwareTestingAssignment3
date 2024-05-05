import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def load_tc_list(path):
  """Load testcases from .json file
  
  Format of the file should be: list[dict]
  """
  with open(path, 'r') as f:
    tc_list = json.load(f)
    retval = list(map(lambda x: tuple(x.values()), tc_list))
  return retval
  

class TestEDITPROFILE():

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


  def test_usecase(self):
    # Usecase Testing using Data-driven approach is not suitable
    # since each testcase is a separate script
    pass

  @pytest.mark.parametrize(
      "firstname, lastname, email"
      , load_tc_list("./EditProfile.Decs.json")
  )
  def test_decision(self, firstname, lastname, email):
    """Decision Table Testing"""

    self.__login()
    self.driver.get("https://school.moodledemo.net//my/courses.php")
    self.driver.find_element(By.CSS_SELECTOR, ".userpicture").click()
    self.driver.find_element(By.LINK_TEXT, "Profile").click()
    self.driver.find_element(By.LINK_TEXT, "Edit profile").click()


    if firstname == "":
      self.driver.find_element(By.ID, "id_firstname").clear()
    else:
      self.driver.find_element(By.ID, "id_firstname").clear()
      self.driver.find_element(By.ID, "id_firstname").send_keys(firstname)
    if firstname == "":
      assert self.driver.find_element(By.ID, "id_error_firstname").text == "- Missing given name"


    if lastname == "":
      self.driver.find_element(By.ID, "id_lastname").clear()
    else:
      self.driver.find_element(By.ID, "id_lastname").clear()
      self.driver.find_element(By.ID, "id_lastname").send_keys(lastname)
    if lastname == "":
      assert self.driver.find_element(By.ID, "id_error_lastname").text == "- Missing last name"


    if email == "":
      self.driver.find_element(By.ID, "id_email").clear()
    else:
      self.driver.find_element(By.ID, "id_email").clear()
      self.driver.find_element(By.ID, "id_email").send_keys(email)  
    if email == "":
      assert self.driver.find_element(By.ID, "id_error_email").text == "- Required"
    

    self.driver.find_element(By.ID, "id_submitbutton").click()

    if email != "" and "@" not in email:
        # invalid email
        if firstname != "" and lastname != "":
          assert self.driver.find_element(By.ID, "id_error_email").text == "Invalid email address"
    else:
        pass
    
    if firstname != "" and lastname != "" and "@" in email:
      assert self.driver.find_element(By.CSS_SELECTOR, "h2:nth-child(2)").text == f"{firstname} {lastname}"
      assert self.driver.find_element(By.ID, "notice").text == "You have requested a change of email address, from jeffreysanders199@example.com to hello@gmail.com. For security reasons, we are sending you an email message at the new address to confirm that it belongs to you. Your email address will be updated as soon as you open the URL sent to you in that message."
      elements = self.driver.find_elements(By.CSS_SELECTOR, ".continuebutton > form")
      assert len(elements) > 0
    else:
      assert self.driver.find_element(By.CSS_SELECTOR, ".breadcrumb-item > span").text == "Edit profile"
    self.driver.close()