import unittest
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# import page


def login(driver, role):
    if not isinstance(role, str):
        raise TypeError('role must be a string')

    login_url = os.environ.get('login_url') or "https://school.moodledemo.net/login/index.php"  # Assuming you have the URL in an environment variable
    driver.get(login_url)
    username_field = driver.find_element(By.ID, 'username')
    username_field.clear()
    username_field.send_keys(role, Keys.TAB, os.environ.get('login_password') or "moodle", Keys.ENTER)

def logout(driver):
    if not driver:
        raise ValueError('Driver cannot be undefined')

    user_menu = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[id='user-menu-toggle']"))
    )
    user_menu.click()

    logout_link = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Log out')]"))
    )
    logout_link.click()

class ParticipantFilter(unittest.TestCase):
    """A sample test class to show how page object works"""
    
        
    def setUp(self):
        options = Options()
        options.add_argument("--enable-chrome-browser-cloud-management")
        self.driver =  webdriver.Edge(service=Service('webdrivers/msedgedriver.exe'), options=options)
        self.driver.implicitly_wait(10)
        # self.driver = webdriver.Chrome(service=ChromeService('webdrivers/chromedriver.exe'))
    

    def test_basicflow(self):
        login(self.driver, "teacher")
        self.driver.find_element(By.XPATH, "//a[@href=\'https://school.moodledemo.net/course/view.php?id=69\']").click()
        self.driver.find_element(By.LINK_TEXT, "Participants").click()
        self.driver.find_element(By.CSS_SELECTOR, "div[data-filterregion=\'filters\'] select[data-filterfield=\'join\'").click()
        dropdown = self.driver.find_element(By.CSS_SELECTOR, "div[data-filterregion=\'filters\'] select[data-filterfield=\'join\' ")
        dropdown.find_element(By.CSS_SELECTOR, "*[value='2']").click()
        self.driver.find_element(By.CSS_SELECTOR, "div[data-filterregion=\'filters\'] select[data-filterfield=\'type\'").click()
        dropdown = self.driver.find_element(By.CSS_SELECTOR, "div[data-filterregion=\'filters\'] select[data-filterfield=\'type\'")
        dropdown.find_element(By.CSS_SELECTOR, "*[value='accesssince']").click()
        self.driver.find_element(By.XPATH, "//div[@data-filterregion=\'value\']//span").click()
        self.driver.find_element(By.XPATH, "//div[@data-filterregion=\'value\']//li[contains(text(), \'2 weeks\')]").click()
        self.driver.find_element(By.CSS_SELECTOR, "button[data-filteraction=\'apply\']").click()
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Apply filters\')]").click()
        WebDriverWait(self.driver, 5).until(expected_conditions.invisibility_of_element_located((By.XPATH, "//*[@id=\"participants\"]//td[contains(text(), \'jeffreysanders199@example.com\')]")))
        WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, "//td[contains(.,\'markellis267@example.com\')]")))
        logout(self.driver)
        self.driver.close()
    
    def test_alternative3Noresultfounded(self):
        login(self.driver, "teacher")
        self.driver.find_element(By.XPATH, "//a[@href=\'https://school.moodledemo.net/course/view.php?id=69\']").click()
        self.driver.find_element(By.LINK_TEXT, "Participants").click()
        self.driver.find_element(By.CSS_SELECTOR, "div[data-filterregion=\'filters\'] select[data-filterfield=\'join\'").click()
        dropdown = self.driver.find_element(By.CSS_SELECTOR, "div[data-filterregion=\'filters\'] select[data-filterfield=\'join\'")
        dropdown.find_element(By.CSS_SELECTOR, "*[value='2']").click()
        self.driver.find_element(By.CSS_SELECTOR, "div[data-filterregion=\'filters\'] select[data-filterfield=\'type\'").click()
        dropdown = self.driver.find_element(By.CSS_SELECTOR, "div[data-filterregion=\'filters\'] select[data-filterfield=\'type\'")
        dropdown.find_element(By.CSS_SELECTOR, "*[value='roles']").click()
        self.driver.find_element(By.XPATH, "//div[@data-filterregion=\'value\']//span").click()
        self.driver.find_element(By.XPATH, "//div[@data-filterregion=\'value\']//li[contains(text(), \'Guest\')]").click()
        self.driver.find_element(By.CSS_SELECTOR, "button[data-filteraction=\'apply\']").click()
        self.vars["count"] = self.driver.find_element(By.CSS_SELECTOR, "#participantsform p[data-region=\'participant-count\']").text
        self.vars["num"] = self.driver.execute_script("return arguments[0].match(/^\\d+/);", self.vars["count"])
        self.assertTrue(self.vars["num"] == 0)
        logout(self.driver)
        self.driver.close()
    
    def test_alternative1Addmultiplefilters(self):
        login(self.driver, "teacher")
        self.driver.find_element(By.XPATH, "//a[@href=\'https://school.moodledemo.net/course/view.php?id=69\']").click()
        self.driver.find_element(By.LINK_TEXT, "Participants").click()
        self.driver.find_element(By.CSS_SELECTOR, "div[data-filterregion=\'filters\'] select[data-filterfield=\'join\'").click()
        dropdown = self.driver.find_element(By.CSS_SELECTOR, "div[data-filterregion=\'filters\'] select[data-filterfield=\'join\' ")
        dropdown.find_element(By.CSS_SELECTOR, "*[value='2']").click()
        self.driver.find_element(By.CSS_SELECTOR, "div[data-filterregion=\'filters\'] select[data-filterfield=\'type\'").click()
        dropdown = self.driver.find_element(By.CSS_SELECTOR, "div[data-filterregion=\'filters\'] select[data-filterfield=\'type\'")
        dropdown.find_element(By.CSS_SELECTOR, "*[value='accesssince']").click()
        self.driver.find_element(By.CSS_SELECTOR, "button[data-filteraction=\'add\']").click()
        self.driver.find_element(By.XPATH, "//fieldset/div/div/select").click()
        dropdown = self.driver.find_element(By.CSS_SELECTOR, "div[data-filterregion=\'filter\']:nth-child(2) select[data-filterfield=\'join\'")
        dropdown.find_element(By.CSS_SELECTOR, "*[value='2']").click()
        self.driver.find_element(By.CSS_SELECTOR, "div[data-filterregion=\'filter\']:nth-child(2) select[data-filterfield=\'type\'").click()
        dropdown = self.driver.find_element(By.CSS_SELECTOR, "div[data-filterregion=\'filter\']:nth-child(2) select[data-filterfield=\'type\'")
        dropdown.find_element(By.CSS_SELECTOR, "*[value='roles']").click()
        self.driver.find_element(By.XPATH, "(//div[@data-filterregion=\'value\'])[2]//span").click()
        self.driver.find_element(By.XPATH, "//div[@data-filterregion=\'value\']//li[contains(text(), \'Student\')]").click()
        self.driver.find_element(By.CSS_SELECTOR, "button[data-filteraction=\'apply\']").click()
        self.driver.find_element(By.CSS_SELECTOR, "a[data-action=\'showcount\']").click()
        WebDriverWait(self.driver, 30).until(expected_conditions.invisibility_of_element_located((By.XPATH, "//*[@id=\"participants\"]//td[contains(text(), \'jeffreysanders199@example.com\')]")))
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//td[contains(.,\'stephanadams175@example.com\')]")))
        logout(self.driver)
        self.driver.close()
    
    def test_alternative2Nofilterbeingfilled(self):
        login(self.driver, "teacher")
        self.driver.find_element(By.XPATH, "//a[@href=\'https://school.moodledemo.net/course/view.php?id=69\']").click()
        self.driver.find_element(By.LINK_TEXT, "Participants").click()
        self.vars["precount"] = self.driver.find_element(By.CSS_SELECTOR, "#participantsform p[data-region=\'participant-count\']").text
        self.vars["prenum"] = self.driver.execute_script("return arguments[0].match(/^\\d+/);", self.vars["precount"])
        self.driver.find_element(By.CSS_SELECTOR, "button[data-filteraction=\'apply\']").click()
        self.vars["postcount"] = self.driver.find_element(By.CSS_SELECTOR, "#participantsform p[data-region=\'participant-count\']").text
        self.vars["postnum"] = self.driver.execute_script("return arguments[0].match(/^\\d+/);", self.vars["postcount"])
        self.assertTrue(self.vars["prenum"] == self.vars["postnum"])
        logout(self.driver)
        self.driver.close()
    
    def test_exceptionUserleavesthesubfieldblank(self):
        login(self.driver, "teacher")
        self.driver.find_element(By.XPATH, "//a[@href=\'https://school.moodledemo.net/course/view.php?id=69\']").click()
        self.driver.find_element(By.LINK_TEXT, "Participants").click()
        self.driver.find_element(By.CSS_SELECTOR, "button[data-filteraction=\'add\']").click()
        WebDriverWait(self.driver, 10).until(expected_conditions.invisibility_of_element_located((By.CSS_SELECTOR, "div[data-filterregion=\'filter\']:nth-child(2)")))
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "div.warning")))
        logout(self.driver)
        self.driver.close()
    
    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()