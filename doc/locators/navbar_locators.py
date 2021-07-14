from selenium.webdriver.common.by import By


class NavBarLocators:
    btn_photo_gallery = (By.XPATH, "//div[@id='navbarNavDropdown']//a[contains(text(), 'Photo Gallery')]")
