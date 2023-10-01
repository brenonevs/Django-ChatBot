from selenium.webdriver.firefox.webdriver import WebDriver
from django.test import LiveServerTestCase
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class MySeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = WebDriver()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_chatbot_functionality(self):
        # Open the home page
        self.driver.get(self.live_server_url)

        # Find the chat button id=chat-button and click it
        chat_button = self.driver.find_element(By.ID, "chat-button")
        chat_button.click()

        time.sleep(4)

        # Check if the user is redirected to the chatbot page
        self.assertIn("Chat com Doutrinator", self.driver.page_source)

        # Find the message input and send button
        message_input = self.driver.find_element(By.CLASS_NAME, "message-input")
        send_button = self.driver.find_element(By.CLASS_NAME, "btn-send")

        # Type a message and send it
        message_input.send_keys(
            "Opa doutrinator! Sou contra o aborto e defendo o homeschooling."
        )
        time.sleep(1)
        send_button.click()

        # Wait for a while to let the response appear
        time.sleep(5)  # it's better to use WebDriverWait (more advanced)

        # Check if the sent message and response are in the messages list
        messages_list = self.driver.find_element(By.CLASS_NAME, "messages-list")
        self.assertIn("Você", messages_list.text)
