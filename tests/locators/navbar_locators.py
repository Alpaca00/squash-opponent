from selenium.webdriver.common.by import By


class NavBarLocators:
    btn_photo_gallery = (By.XPATH, "//a[contains(text(), 'Photo-Gallery')]")
    btn_finder_opponent = (By.XPATH, "//a[contains(text(), 'Finder-Opponent')]")
    btn_support = (By.XPATH, "//div[@id='navbarNavDropdown']//a[contains(text(), 'Support')]")
    btn_login = (By.XPATH, "//*[@id='btn-login-unique']")
    btn_logout = (By.XPATH, "//a[contains(text(), 'Logout')]")
