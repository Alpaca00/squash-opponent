from selenium.webdriver.common.by import By


class UserCardLocators:
    email_info = (By.XPATH, "//div[@id='user-card-email']/h6")
    phone_field = (By.XPATH, "//input[@id='user-phone']")
    location_select = (By.XPATH, "//select[@id='location-select']")
    category_select = (By.XPATH, "//select[@id='category-select']")
    date_field = (By.XPATH, "//input[@id='party']")
    post_btn = (By.XPATH, "//input[@class='post-btn']")

    class History:
        all_delete_post_btn = (By.XPATH, "//a[@id='delete-post-opponent']")

    class DisplayAlertInfo:
        alert_info = (By.XPATH, "//*[@class='alert alert-info']")
