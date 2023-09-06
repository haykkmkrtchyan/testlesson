import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class SoftAssert(unittest.TestCase):
    def __init__(self):
        super().__init__()
        self.soft_assert_errors = []

    def soft_assert(self, condition, message=None):
        try:
            self.assertTrue(condition, message)
        except AssertionError as e:
            self.soft_assert_errors.append(str(e))

    def assert_all(self):
        if self.soft_assert_errors:
            error_message = "\n".join(self.soft_assert_errors)
            self.fail(f"SoftAssert failed:\n{error_message}")

class TestYouTube(unittest.TestCase):  # Убрали наследование от SoftAssert

    def setUp(self) -> None:
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.delete_all_cookies()
        self.driver.get("https://www.youtube.com/")
        time.sleep(2)

        inputFieldElement = self.driver.find_element(By.XPATH, "(//input[@id=\"search\"])")
        inputFieldElement.clear()
        inputFieldElement.send_keys("Armenian Football National Team")
        inputFieldElement.send_keys(Keys.ENTER)
        time.sleep(2)

        clickFirstVideo = self.driver.find_element(By.LINK_TEXT, "Armenia | National Football Team 2023")
        clickFirstVideo.click()
        time.sleep(2)
        pauseVideoPlayer = self.driver.find_element(By.ID, "player")
        pauseVideoPlayer.click()
        time.sleep(2)

    def test_firstVideo(self):
        clickFirstElement = self.driver.find_element(By.XPATH, "(//a[@class=\"yt-simple-endpoint style-scope ytd-compact-video-renderer\"])[1]")
        clickFirstElement.click()
        time.sleep(2)

        soft_assert = SoftAssert()  # Создаем экземпляр SoftAssert
        soft_assert.soft_assert("test" == self.driver.title, "The title is not test")
        soft_assert.soft_assert(3 == 3, "3 is equal to 3")
        soft_assert.soft_assert(3 == 4, "3 is not equal to 4")
        soft_assert.assert_all()

    def tearDown(self) -> None:
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
