from selenium.webdriver.common.by import By


class PhotoGalleryLocators:
    lst_images = (By.XPATH, "//div[@class='container-lg']//img")
    modal_window = (By.XPATH, "//div[@class='modal-body']/img")
    modal_window_title = (By.XPATH, "//*[@id='exampleModalLabel']")
