from selenium.webdriver.common.by import By


class NavBarLocators:
    btn_photo_gallery = (By.XPATH, "//div[@id='navbarNavDropdown']//a[contains(text(), 'Photo Gallery')]")
    btn_support = (By.XPATH, "//div[@id='navbarNavDropdown']//a[contains(text(), 'Support')]")

    class Action:
        btn_action = (By.XPATH, "//*[@id='navbarDropdownMenuLink']")
        btn_login = (By.XPATH, "//*[@id='btn-login-unique']")
