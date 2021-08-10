import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from loguru import logger
from db import db_main as db


#chrome_options.add_argument("user-data-dir=selenium") 

#LOGIN = "maximoous4@gmail.com"
#PASS = "Melbet007123"

#LOGIN = "301357285"
#PASS = "86Yx52"

LOGIN = "aga.ugu.11@gmail.com"
PASS = "Aga007123"

#LOGIN = "296453143"
#PASS = "Melbet007123"

#LOGIN = "16601693"
#PASS = "Qq261961"

    #document.getElementById("auth_id_email").value = "{LOGIN}";
    #document.getElementById("auth-form-password").value = "{PASS}";
def login(driver):
    try:
        driver.execute_script("""
    document.getElementsByClassName("js-reg")[0].click()
    """)
        time.sleep(5)
        driver.find_element_by_id("auth_id_email").send_keys(LOGIN)
        driver.find_element_by_id("auth-form-password").send_keys(PASS)
        driver.execute_script(f"""
    document.getElementById("remember_user").checked = true;
    document.getElementsByClassName("auth-button")[0].click()
    """)
    except Exception as e:
        pass
def mob_get_id(driver):
    driver.get("https://m.melbet.com/casino/?products=%5B46%5D")
    time.sleep(10)
    login(driver)
    time.sleep(10)
    driver.execute_script("""
document.getElementsByClassName("sl-casino__layer")[0].click();
""")
    time.sleep(5)
    try:
        driver.execute_script("""
        document.getElementsByClassName("swal2-confirm")[0].click();
        """)
    except Exception as e:
        pass
    time.sleep(5)
    for cookie in driver.get_cookies():
        if cookie["name"] == "EVOSESSIONID":
            logger.debug(cookie["value"])
            driver.get("https://google.com")
            return cookie["value"]

@logger.catch
def parse_evo_id():
    driver = webdriver.Remote(
       command_executor='http://chrome:4444',
       desired_capabilities=DesiredCapabilities.CHROME)
    while True:
        try:
            sess_id = mob_get_id(driver)
            if sess_id:
                with open("sess_id.txt","w") as file:
                    file.write(sess_id)
                    file.close()
                    db.set_evo_id(sess_id)
            time.sleep(120)
        except Exception as e:
            logger.error(e)
