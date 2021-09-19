from selenium.webdriver.common.by import By


class UserCardLocators:
    email_info = [(By.XPATH, "//div[@id='user-card-email']/h6"), (By.CSS_SELECTOR, "#user-card-email h6")]
    phone_field = (By.XPATH, "//input[@id='user-phone']")
    location_select = (By.XPATH, "//select[@id='location-select']")
    category_select = (By.XPATH, "//select[@id='category-select']")
    date_field = (By.XPATH, "//input[@id='party']")
    post_btn = (By.XPATH, "//input[@class='post-btn']")

    class History:
        all_delete_post_btn = (By.XPATH, "//a[@id='delete-post-opponent']")
        all_change_post_btn = (By.XPATH, "//a[@id='change-post-opponent']")
        all_rows_opponent_post_information_phone_text_at_card = (
            By.XPATH, "//a[@id='change-post-opponent']/../../ul/li[contains(text(),'Phone')]"
        )
        all_rows_opponent_post_information_category_text_at_card = (
            By.XPATH, "//a[@id='change-post-opponent']/../../ul/li[contains(text(),'Category')]"
        )
        all_rows_opponent_post_information_district_text_at_card = (
            By.XPATH, "//a[@id='change-post-opponent']/../../ul/li[contains(text(),'District')]"
        )

    class DisplayAlertInfo:
        alert_info = (By.XPATH, "//*[@class='alert alert-info']")
