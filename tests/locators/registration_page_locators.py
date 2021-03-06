from selenium.webdriver.common.by import By


class RegistrationFormLocators:
    email_field = (By.XPATH, "//*[@id='email-id']")
    name_field = (By.XPATH, "//*[@id='name-id']")
    password_field = (By.XPATH, "//*[@id='password-id']")
    submit_btn = (By.XPATH, "//button[contains(text(), 'SUBMIT')]")

    class ConfirmPageLocators:
        account_confirm_link = (By.XPATH, "//a[@href='/en/register/resend']")
