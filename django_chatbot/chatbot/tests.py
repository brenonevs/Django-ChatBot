from selenium.webdriver.firefox.webdriver import WebDriver
from django.test import LiveServerTestCase
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .models import Character


class ChatSeleniumTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = WebDriver()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        Character.objects.create(
            name="Doutrinator",
            description="Personagem padrão que tenta adivinhar sua ideologia.",
            prompt="Você é Doutrinator, um político especialista capaz de identificar a ideologia de qualquer pessoa a partir do que ela diz. Após a primeira frase dela, você deve dizer sua ideologia política.",
            chat_model_name="gpt-3.5-turbo-0613",
        )

    def test_chatbot_functionality(self):
        # Open the home page
        self.driver.get(self.live_server_url)

        # Find the chat button id=chat-button and click it
        chat_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "chat-button"))
        )
        chat_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, "body"), "Chat com Doutrinator"
            )
        )

        # Find the message input and send button
        message_input = self.driver.find_element(By.CLASS_NAME, "message-input")
        send_button = self.driver.find_element(By.CLASS_NAME, "btn-send")

        # Type a message and send it
        message_input.send_keys(
            "Opa doutrinator! Sou contra o aborto e defendo o homeschooling."
        )
        send_button.click()

        # Wait for the message to be sent and the response to arrive
        WebDriverWait(self.driver, 20).until(
            lambda driver: len(
                driver.find_elements(By.CSS_SELECTOR, ".messages-list li")
            )
            >= 3
        )

        # Check if there are three messages in the messages list
        messages_list = self.driver.find_elements(By.CSS_SELECTOR, ".messages-list li")
        self.assertEqual(len(messages_list), 3)
