from selenium.webdriver.common.by import By


class LoginLocators:
    sign_up = (By.XPATH, "//*[@id='sign-up-unique']")
    email_field = (By.XPATH, "//input[@placeholder='email']")
    password_field = (By.XPATH, "//input[@placeholder='password']")
    remember_me_checkbox = (By.XPATH, "//input[@id='remember-me']")
    submit_login = (By.XPATH, "//input[@id='submit-user-login']")
