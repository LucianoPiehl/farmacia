from datetime import time
import time
from selenium.webdriver.common.by import By


def recopilacion_precios_suizo(driver,descripciones, codigos):
    precios = []
    # BUSCA PRECIOS DE LOS PRODUCTOS QUE RECIBE POR PARAMETRO EN SUIZO
    elementos = driver.find_elements(By.TAG_NAME, "a")
    elementos[7].click()
    time.sleep(4)
    for i in codigos:

        input_element = driver.find_element(By.ID, "codigo")
        input_element.click()
        input_element.send_keys(i)
        # Le doy al boton buscar
        boton_buscar = driver.find_elements(By.NAME, "buscarbtn")
        boton_buscar[1].click()
        time.sleep(2)
        # Recopilacion y procesamiento de stock
        td_element = driver.find_elements(By.TAG_NAME, "td")
        # 8,9,11

        try:
            precios.append(td_element[9].text)
            driver.back()
            time.sleep(2)
        except:
            pass


    return descripciones, precios


def recopilacion_precios_sud(driver, descripciones, codigos):
    time.sleep(11)
    precios = []
    input_element = driver.find_element(By.XPATH,
                                        "//input[@placeholder='Descripción/Código'][contains(@class, 'valid')]")
    input_element.send_keys("asda")

    # Localiza el elemento por XPath usando el type y el value como referencia
    submit_button = driver.find_element(By.XPATH, "//input[@type='submit'][@value='Buscar']")
    submit_button.click()
    input_element.clear()
    for ind,i in enumerate(codigos):
        input_element = driver.find_element(By.ID, "SearchFilterValues_DescriptionSearch")
        input_element.send_keys(i)
        submit_button = driver.find_element(By.ID, "find")
        submit_button.click()
        time.sleep(1)
        input_element.clear()

        td_elements = driver.find_elements(By.TAG_NAME, "td")


        try:
            precios.append(td_elements[9].text)
        except:
            pass
    return descripciones,precios



