from selenium.webdriver.common.by import By


class SupportLocators:
    question_field = (By.XPATH, "//*[@id='reg-form']//input[@name='question']")
    email_field = (By.XPATH, "//*[@id='reg-form']//input[@name='email']")
    subject_field = (By.XPATH, "//*[@id='reg-form']//input[@name='subject']")
    text_field = (By.XPATH, "//*[@id='reg-form']//input[@name='text']")
    btn_submit = (By.XPATH, "//*[@id='reg-form']//*[contains(text(),'submit')]")
