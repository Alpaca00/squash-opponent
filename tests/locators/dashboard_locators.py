from selenium.webdriver.common.by import By


class AdminLoginPageLocators:
    username = (By.XPATH, "//input[@id='username']")
    password = (By.XPATH, "//input[@id='password']")
    remember = (By.XPATH, "//input[@id='remember']")
    btn_login = (By.XPATH, "//button[contains(text(),'Login')]")


class AdminNavBarLocators:
    btn_support = (By.XPATH, "//div[@class='container']//a[contains(text(), 'Support')]")
    # btn_user_account = (By.XPATH, "//a[contains(text(),'User Account')]")
    btn_user_account = (By.XPATH, "/html/body/div/nav/div/ul[1]/li[2]/a")

    class UserAccountTable:
        column_email = (By.XPATH, "//td[@class='col-email']")
