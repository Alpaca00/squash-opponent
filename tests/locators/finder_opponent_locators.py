from selenium.webdriver.common.by import By


class FinderOpponentLocators:
    btns_offer = (By.XPATH, "//*[@id='offer-show-modal']")
    alert_offer = (By.XPATH, "//*[@id='alert-offer']")
    alert_accept = (By.XPATH, "//*[@id='alert-accept']")

    class OfferModalWindow:
        label = (By.XPATH, "//*[@id='exampleModalLabel']")
        name_field = (By.XPATH, "//input[@id='user-name']")
        email_field = (By.XPATH, "//input[@id='user-email']")
        phone_field = (By.XPATH, "//input[@id='user-phone']")
        location_select = (By.XPATH, "//select[@id='location-select']")
        category_select = (By.XPATH, "//select[@id='category-select']")
        message_text = (By.XPATH, "//*[@id='message-text']")
        date_picker = (By.XPATH, "//input[@id='party']")
        send_btn = (By.XPATH, "//input[@id='blockBtn']")

    class MessageWidget:
        label = (By.XPATH, "//div[@class='pop-up-content-wrap']/h6")
        text_message = (By.XPATH, "//div[@class='pop-up-content-wrap']/p")
