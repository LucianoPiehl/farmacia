import time
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

from auxiliar import obtener_codigo, ir_a_carrito_suizo, obtener_cantidades_suizo, obtener_descripciones_suizo, \
    dirigirse_a_buscar, ir_a_carrito_sud, obtener_descripciones_sud, obtener_cantidades_sud, obtener_descripcion


def extraer_descripciones_suizo(driver):
    ir_a_carrito_suizo(driver)
    productos = obtener_descripciones_suizo(driver)
    return driver,productos
def extraer_carrito_suizo(driver,productos):
    # Establezco las variables en donde se guardaran los datos en forma de lista
    codigos = []
    cantidades = obtener_cantidades_suizo(driver)
    dirigirse_a_buscar(driver)


    for m in productos:
        texto_busqueda = m
        producto_encontrado = False
        # Recorre el texto del producto mientras no lo encuentre buscandoló (Restando caracteres)
        while texto_busqueda and not producto_encontrado:
            # Busca el elemento con la cantidad de caracteres necesaria
            # Hacer clic en el campo de texto 'empieza'

            consulta_stock = driver.find_element(By.XPATH, "//h2[text()='Consulta de stock']")
            consulta_stock.click()

            time.sleep(2)
            #print(driver.current_url)
            buscador_input = driver.find_element(By.XPATH, "//input[@placeholder='Letras con que empieza']")
            buscador_input.click()
            buscador_input.clear()  # Limpia el campo antes de enviar el nuevo texto
            buscador_input.send_keys(texto_busqueda)

            # Enviar la tecla ENTER
            buscador_input.send_keys(Keys.ENTER)
            time.sleep(2)

            # Intenta encontrar el elemento "Detalles"
            elemento_detalles = driver.find_elements(By.XPATH, "//td[@class='t1 filtro-b']")
            time.sleep(4)

            elemento_advertencia_presente = False
            try:
                driver.find_element(By.XPATH, "//div[contains(@class, 'warning')]")
                elemento_advertencia_presente = True
            except NoSuchElementException:
                # Si no se encuentra el elemento de advertencia, no hagas nada aquí
                pass

            if elemento_advertencia_presente:
                texto_busqueda = texto_busqueda[:-3]  # Reduce el texto de búsqueda solo si se encontró el elemento de advertencia
                continue

            if len(elemento_detalles) == 1:
                datos = elemento_detalles[0].get_attribute("onmouseover")
                codigos_texto = obtener_codigo(datos)
                descripcion = obtener_descripcion(datos)
                # Agrega todos los elementos a codigos
                # print(f"Tiene un solo resultado: {codigos_texto}")

                if m.replace(" ", "") in descripcion[0].replace(" ", ""):
                    codigos.append(codigos_texto)
                # Está variable es para hacer doble break. Ya que ya se encontró el producto
                break

            else:
                for ind,n in enumerate(elemento_detalles):
                    ActionChains(driver).move_to_element(n).perform()
                    time.sleep(4)

                    datos = n.get_attribute("onmouseover")
                    codigos_texto = obtener_codigo(datos)
                    descripcion = obtener_descripcion(datos)
                    # Agrega todos los elementos a codigos
                    # print(f"Tiene un solo resultado: {codigos_texto}")

                    if m.replace(" ", "") in descripcion[0].replace(" ", ""):
                        codigos.append(codigos_texto)
                    #(f"Tiene un solo resultado N°: {ind} {codigos_texto.text}")

                break



    return driver, codigos, cantidades




def extraer_descripciones_sud(driver):
    ir_a_carrito_sud(driver)
    descripciones=obtener_descripciones_sud(driver)
    # Recorta de las descripciones y spans 16 elementos que son spans que no son nombres de productos
    descripciones = descripciones[16:]
    return driver, descripciones




def extraer_carrito_sud(driver,descripciones):

    codigos = []
    time.sleep(5)
    spans = descripciones
    cantidades=obtener_cantidades_sud(driver)

    # Recorre cada producto
    for indice, span in enumerate(spans):
        time.sleep(3)
        texto_busqueda = span
        producto_encontrado = False
        salir_bucles = False
        # Recorre el texto del producto mientras no lo encuentre buscandoló (Restando caracteres)
        while texto_busqueda and not producto_encontrado:
            # Busca el elemento con la cantidad de caracteres necesaria
            input_element = driver.find_element(By.ID, "SearchFilterValues_DescriptionSearch")
            input_element.clear()
            input_element.send_keys(texto_busqueda)
            boton_buscar = driver.find_element(By.ID, "find")
            boton_buscar.click()
            time.sleep(4)

            # Intenta encontrar el elemento "Detalles"
            elemento_detalles = driver.find_elements(By.XPATH,
                                                     "//span[@class='itemTooltip' and contains(text(), 'Detalles')]")

            # Si solo hay un elemento de detalle, osea si solo hay un producto como resultado
            if len(elemento_detalles) == 1:
                # Recorro cada elemento porque estoy utilizando find_elements
                for i in elemento_detalles:
                    # Muevo el cursor a el elemento detalles y le doy click
                    # para que se despliegue el html en donde esta el codigo de barras
                    ActionChains(driver).move_to_element(i).click().perform()
                    time.sleep(2)

                    # Obtiene el código de barras y otros elementos que no sirven
                    codigos_texto = driver.find_elements(By.XPATH,
                                                         "//label[contains(text(), 'Codigo de barra:')]/following-sibling::label[@class='res']")
                    descripcion = driver.find_elements(By.XPATH,
                                                       "//label[contains(text(), 'Descripción:')]/following-sibling::label[@class='res']")

                    # Agrega todos los elementos a codigos
                    for ind, l in enumerate(codigos_texto):
                        #print(f"Tiene un solo resultado: N° {ind} {str(l.text)}")
                        if l.text != '' and descripcion[ind] in descripciones:
                            codigos.append(l.text)
                    # Está variable es para hacer doble break. Ya que ya se encontró el producto
                    salir_bucles = True
                    break

            elif len(elemento_detalles) == 0:
                texto_busqueda = texto_busqueda[:-3]
                continue
            else:
                for m in elemento_detalles:
                    ActionChains(driver).move_to_element(m).click().perform()
                    time.sleep(4)

                    codigos_texto = driver.find_elements(By.XPATH,
                                                         "//label[contains(text(), 'Codigo de barra:')]/following-sibling::label[@class='res']")

                    descripcion = driver.find_elements(By.XPATH,
                                                       "//label[contains(text(), 'Descripción:')]/following-sibling::label[@class='res']")

                    input_element = driver.find_element(By.ID, "SearchFilterValues_DescriptionSearch")
                    input_element.click()

                    for indice2, k in enumerate(codigos_texto):
                        if k.text != '' and descripcion[indice2] in descripciones:
                            codigos.append(k.text)

                break
            if salir_bucles:
                break



    descripciones = [elemento for elemento in descripciones if elemento != ""]
    return driver, codigos, cantidades


def extraer_carrito_sur():
    pass


def extraer_carrito_monroe():
    pass
