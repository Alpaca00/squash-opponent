from selenium.webdriver.common.by import By


class FinderOpponentLocators:
    btns_offer = (By.XPATH, "//*[@id='offer-show-modal']")
    alert_offer = (By.XPATH, "//*[@id='alert-offer']")
    alert_accept = (By.XPATH, "//*[@id='alert-accept']")
