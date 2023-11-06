from django.urls import reverse
from django.contrib.auth import get_user_model
from selenium.webdriver.firefox.webdriver import WebDriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .models import Character

User = get_user_model()


class ChatSeleniumTestCase(StaticLiveServerTestCase):
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

    def test_chatbot(self):
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


class SignupSeleniumTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls) -> None:
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

    def test_signup(self):
        # Open the signup page
        self.driver.get(self.live_server_url + reverse("signup"))

        # Wait for the signup form to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "field_username"))
        )

        # Find the signup form inputs
        username_input = self.driver.find_element(By.ID, "field_username")
        email_input = self.driver.find_element(By.ID, "field_email")
        password1_input = self.driver.find_element(By.ID, "field_password1")
        password2_input = self.driver.find_element(By.ID, "field_password2")
        signup_button = self.driver.find_element(By.ID, "input_submit")

        # Fill out the form
        username_input.send_keys("testuser")
        email_input.send_keys("testuser@example.com")
        password1_input.send_keys("myhardveryhardpassword")
        password2_input.send_keys("myhardveryhardpassword")

        # Submit the form
        signup_button.click()

        # Wait for the signup to complete and check that has been redirected to the chatbot page
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, "body"), "Chat com Doutrinator"
            )
        )

        # verify that the user was created in the database and that it is logged in
        self.assertEqual(User.objects.count(), 1)
        try:
            user = User.objects.get(username="testuser")
        except User.DoesNotExist:
            self.fail("User was not created.")

        self.assertEqual(user.username, "testuser")  # type: ignore

        # Check if the user is logged in through cookie. watchout because there are other cookies
        # in the page
        cookies = self.driver.get_cookies()
        session_cookie = next(
            (cookie for cookie in cookies if cookie["name"] == "sessionid"), None
        )

        # Check that the sessionid cookie is present
        self.assertIsNotNone(session_cookie, "Session cookie should be set after login")

        # Optionally, check that the sessionid cookie is not empty
        self.assertNotEqual(session_cookie["value"], "", "Session cookie should not be empty")  # type: ignore
