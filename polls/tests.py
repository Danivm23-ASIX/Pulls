from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


class MySeleniumTests(StaticLiveServerTestCase):
    # Cargamos la base de datos de test
    fixtures = ['testdb.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        # No forzamos headless aquí: se controla con MOZ_HEADLESS=1
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login_ok(self):
        # Accedemos a la página de login del admin
        self.selenium.get(f'{self.live_server_url}/admin/login/')

        # Comprobamos el título de la página
        self.assertEqual(
            self.selenium.title,
            "Log in | Django site admin"
        )

        # Introducimos credenciales correctas
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('admin')

        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('admin123')

        self.selenium.find_element(
            By.XPATH, '//input[@value="Log in"]'
        ).click()

        # Verificamos que hemos entrado correctamente
        self.assertEqual(
            self.selenium.title,
            "Site administration | Django site admin"
        )

    def test_login_error(self):
        # Accedemos a la página de login
        self.selenium.get(f'{self.live_server_url}/admin/login/')

        self.assertEqual(
            self.selenium.title,
            "Log in | Django site admin"
        )

        # Introducimos credenciales incorrectas
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('usuari_no_existent')

        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('contrasenya_incorrecta')

        self.selenium.find_element(
            By.XPATH, '//input[@value="Log in"]'
        ).click()

        # Comprobamos que NO hemos entrado
        self.assertNotEqual(
            self.selenium.title,
            "Site administration | Django site admin"
        )
