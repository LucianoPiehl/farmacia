import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


def agregar_a_carrito_sud(driver, lista_sud, cantidades):
    vaciar_carrito_link = driver.find_element(By.ID, "emptyShoppingCartLink")
    vaciar_carrito_link.click()
    aceptar_button = driver.find_element(By.XPATH, "//span[@class='ui-button-text' and contains(text(), 'Aceptar')]")

    # Da click en el elemento encontrado
    aceptar_button.click()
    for ind, i in enumerate(lista_sud):
        input_element = driver.find_element(By.ID, "SearchFilterValues_DescriptionSearch")
        input_element.send_keys(i)
        submit_button = driver.find_element(By.ID, "find")
        submit_button.click()
        time.sleep(1)
        input_element.clear()
        input_element = driver.find_element(By.CSS_SELECTOR, 'input.itemQuantity.valid')
        # Limpia el contenido actual del input
        input_element.clear()
        # Añade el valor '2' al input
        input_element.send_keys(cantidades[ind])
        # Envía la tecla Enter
        input_element.send_keys(Keys.ENTER)
def agregar_a_carrito_suizo(driver, lista_suizo, cantidades):

    time.sleep(2)
    mis_carros = driver.find_element(By.XPATH, "//a[@href='https://web1.suizoargentina.com/carro']")
    mis_carros.click()
    time.sleep(2)
    boton_vaciar_carro = driver.find_element(By.CLASS_NAME, "vaciarPedidoBtn")
    boton_vaciar_carro.click()
    time.sleep(2)  # Ejemplo de espera simple, ajusta según necesidad

    # Cambia al contexto de la alerta
    alert = driver.switch_to.alert

    # Acepta la alerta
    alert.accept()
    time.sleep(5)
    enlace_stock = driver.find_element(By.LINK_TEXT, "Stock")
    enlace_stock.click()
    time.sleep(2)
    for ind,i in enumerate(lista_suizo):
        # try:
        input_element = driver.find_element(By.XPATH, "//input[@placeholder='Letras con que empieza']")
        input_element.click()
        input_element.send_keys(i)
        time.sleep(2)
        # Le doy al boton buscar
        boton_buscar = driver.find_element(By.NAME, "buscarbtn")
        boton_buscar.click()
        time.sleep(2)
        # Localiza el input por su clase 'cant'
        input_element = driver.find_element(By.CLASS_NAME, 'cant')

        # Limpia el contenido actual del input
        input_element.clear()

        # Añade el valor '2' al input
        input_element.send_keys(cantidades[ind])

        # Envía la tecla Enter
        input_element.send_keys(Keys.ENTER)







