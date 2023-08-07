import re
import time
import logging
from hapanapi.driver_tools import driver_init, CHROME_PATH, CHROME_BIN
from hapanapi.parsers import schedule_date_parser
from selenium.webdriver.common.by import By


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger("HapanaINIT")


class Hapana:
    def __init__(self, username, password, driver=None):
        self.username = username
        self.password = password
        if not driver:
            self.driver = driver_init(CHROME_PATH=CHROME_PATH, CHROME_BIN=CHROME_BIN)
        else:
            self.driver = driver

        # First Timer Report
        self.trial_present_sessions = {}

    def login(self, platform='core'):
        self.driver.get(f"https://{platform}.hapana.com/")
        time.sleep(2)
        if platform == 'grow':
            logger.info("Unable to login, please re-code this again")
        else:
            self.driver.find_element(By.NAME, 'email').send_keys(self.username)
            self.driver.find_element(By.NAME, 'password').send_keys(self.password)
            self.driver.find_element(By.ID, "signin").click()
        time.sleep(2)

    def add_client(self, first_name, last_name, email, phone, platform='core'):
        if platform == 'core':
            self.driver.get("https://core.hapana.com/index.php?route=dashboard/clients/addclientnewpayment&pageurl=clients&from=home")
            time.sleep(2)
            self.driver.find_element(By.ID, 'first_name').send_keys(first_name)
            self.driver.find_element(By.ID, 'last_name').send_keys(last_name)
            self.driver.find_element(By.ID, 'email').send_keys(email)
            self.driver.find_element(By.ID, 'phone').send_keys(phone)
            self.driver.find_element(By.ID, "btn-add-client").click()
            time.sleep(2)
        elif platform =='grow':
            self.driver.get("https://grow-api.hapana.com/widget/form/vIYNBYCfx0mIl8DJr1fL")
            time.sleep(1)
            self.driver.find_element(By.NAME, 'first_name').send_keys(first_name)
            self.driver.find_element(By.NAME, 'last_name').send_keys(last_name)
            self.driver.find_element(By.NAME, 'email').send_keys(email)
            self.driver.find_element(By.NAME, 'phone').send_keys(phone)
            # self.driver.find_element(By.CLASS_NAME, "btn").click()
        else:
            logger.info("Wrong platform specified, client not added")

    def schedule(self, date):
        today, day, day_of_week = schedule_date_parser(date)
        self.driver.get("https://core.hapana.com/index.php?route=dashboard/schedule")
        time.sleep(2)
        elems = self.driver.find_elements(By.XPATH,
                                          f"//div[@class='fc-content-skeleton']/table/tbody/tr[1]/td[{day_of_week}]/div[@class='fc-content-col']/div[@class='fc-event-container']/a")
        time.sleep(1)
        session_ids = [elem.get_attribute('href').split("=")[-1] for elem in elems]
        for session_id in session_ids:
            link = f"https://core.hapana.com/index.php?route=dashboard/schedule&seid={session_id}&dt={day}&eid={session_id}&curr={today}"
            self.driver.get(link)
            time.sleep(2)
            class_name = self.driver.find_element(By.XPATH, f"//div[@id='eventLoad']/div[1]/h4").text
            class_name = re.sub('[^A-Za-z0-9 ]+', '', class_name)
            user_table = self.driver.find_elements(By.XPATH,
                                              f"//ul[@id='attendeesList']/li[contains(@class,'d-lg-block')]")
            if len(user_table) < 1:
                logger.info(f"{class_name} is empty!")
            else:
                for item in user_table[1:]:
                    cols = item.find_elements(By.TAG_NAME, "div")
                    visits = cols[1].find_element(By.CLASS_NAME, "milestone").get_attribute('innerText')
                    try:
                        if int(visits) > 1:
                            continue
                    except Exception as e:
                        print(f"Error: {e} detected in {class_name}")
                        continue
                    name = cols[1].find_element(By.TAG_NAME, "a").get_attribute('innerText')
                    name = re.sub('[^A-Za-z0-9 ]+', '', name)
                    package_name = cols[5].find_element(By.TAG_NAME, "span").get_attribute('innerText')
                    if "ClassPass" in package_name:
                        package_name = "ClassPass"
                    else:
                        booked_sessions = re.findall("\(\d{1,}\/\d{1,}\)", package_name)
                        if len(booked_sessions) > 0:
                            booked_pattern = "\\" + booked_sessions[0][:-1] + "\\" + booked_sessions[0][-1]
                            package_name = re.sub(booked_pattern, '', package_name)
                            # num, denom = booked_sessions[0].strip("()").split("/")

                    # home_location = cols[1].find_element(By.XPATH, f"//span[@aria-label='Home Location Alert']")
                    # print(home_location.get_attribute('style'))
                    if class_name not in self.trial_present_sessions:
                        self.trial_present_sessions[class_name] = [
                            {"name": name, "package": package_name, "visits": int(visits)}]
                    else:
                        self.trial_present_sessions[class_name].append(
                            {"name": name, "package": package_name, "visits": int(visits)})
                    print({
                        "name": name,
                        "visits": visits,
                        "package": package_name
                    })

