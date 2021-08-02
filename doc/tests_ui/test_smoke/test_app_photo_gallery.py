import pytest
from selene import have, be, query
from doc.locators.navbar_locators import NavBarLocators
from doc.locators.photo_gallery_locators import PhotoGalleryLocators


class TestPhotoGallery:
    navbar_locator = NavBarLocators()
    photo_gallery_locator = PhotoGalleryLocators()

    def test_click_on_photo_gallery(self, user):
        user.open("/").element(self.navbar_locator.btn_photo_gallery).hover().should(
            have.exact_text("Photo Gallery")
        )
        user.open("/").element(self.navbar_locator.btn_photo_gallery).click()
        assert user.driver.title == "Gallery"

    @pytest.mark.parametrize("item", [0, 2, 4])
    def test_click_on_image_and_wait_for_the_modal_window(self, user, item):
        user.open("/gallery").all(self.photo_gallery_locator.lst_images)[item].click()
        user.element(self.photo_gallery_locator.modal_window).should(be.visible)
        model_window_title = user.element(
            self.photo_gallery_locator.modal_window_title
        ).get(query.text)
        assert model_window_title == "Our team"