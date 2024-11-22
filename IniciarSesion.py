import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def iniciar_sesion_suizo():
    # Inicia ChromeDriver con la versión correcta
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    username = os.getenv("USER_SUIZO")
    password = os.getenv("PASS_SUIZO")
    url = os.getenv("URL_SUIZO")
    driver.get(url)
    time.sleep(4)
    # Recopilo todos los inputs del inicio de sesion
    inputs = driver.find_elements(By.TAG_NAME, "input")

    # Escribo el usuario
    inputs[0].click()
    inputs[0].send_keys(username)

    # Escribo la contraseña
    inputs[1].click()
    inputs[1].send_keys(password)
    time.sleep(20)
    # Le doy a click a login
    inputs[3].click()

    return driver


def iniciar_sesion_sud():
    # Inicia ChromeDriver con la versión correcta

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    username = os.getenv("USER_SUIZO")
    password = os.getenv("PASS_SUIZO")
    url = os.getenv("URL_SUIZO")
    driver.get(url)
    time.sleep(5)

    # Recopilo todos los inputs del inicio de sesion
    inputs = driver.find_elements(By.TAG_NAME, "input")
    # Escribo el usuario
    inputs[2].click()
    inputs[2].send_keys(username)
    inputs[3].click()
    inputs[3].send_keys(password)
    time.sleep(55)
    # No puedo usar tiempo espera implicito por captcha

    # Encuentra el botón por su valor y haz clic en él
    ingresar_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Ingresar']")
    ingresar_button.click()
    time.sleep(4)
    try:
        boton_cerrar = driver.find_element(By.XPATH, "//button[@title='close']")
        boton_cerrar.click()
    except:
        pass
    time.sleep(4)
    return driver

