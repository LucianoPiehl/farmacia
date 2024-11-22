import re
import time
import openpyxl
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By



def obtener_cantidades_sud(driver):
    cantidades=[]
    carro_contenedor = driver.find_element(By.CLASS_NAME, "carroCont")

    # Dentro del contenedor div, busca el input por su clase
    input_cantidad = carro_contenedor.find_elements(By.CLASS_NAME, "shoppingCartItemQuantity")

    # Itera sobre cada input para extraer su valor
    for input_element in input_cantidad:
        value = input_element.get_attribute('value')
        cantidades.append(value)  # Imprime el valor de cada input
    return cantidades

def obtener_descripciones_sud(driver):
    descripciones=[]
    # Encuentra todos los elementos 'span' y los guarda en descripciones
    spans = driver.find_elements(By.TAG_NAME, "span")
    for i in spans:
        descripciones.append(i.text)
    return descripciones

def ir_a_carrito_sud(driver):
    # Localiza boton Comprar
    desplegable = driver.find_element(By.LINK_TEXT, "COMPRAR")

    # Utiliza ActionChains para mover el cursor sobre COMPRAR
    action = ActionChains(driver)
    action.move_to_element(desplegable).perform()
    time.sleep(6)

    # Una vez el mouse está ahi le da a "Armado de pedido"
    armado_pedido_xpath = "//a[contains(@class, 'navigableMenuItem') and contains(text(), 'Armado de pedido')]"
    armado_pedido_link = driver.find_element(By.XPATH, armado_pedido_xpath)
    armado_pedido_link.click()
    time.sleep(5)

def dirigirse_a_buscar(driver):
    # Hacer clic en el botón 'Stock'
    stock_button = driver.find_element(By.XPATH, "//a[@href='https://web1.suizoargentina.com/stock']")
    stock_button.click()
    empieza_input = driver.find_element(By.ID, "empieza")
    empieza_input.click()
    empieza_input.send_keys("actro")
    # Hacer clic en el botón 'Buscar'
    buscar_button = driver.find_element(By.NAME, "buscarbtn")
    buscar_button.click()

def obtener_descripciones_suizo(driver):
    productos = []
    contador = 0
    elemento = driver.find_element(By.XPATH, "//a[contains(text(), 'Mis carros')]")

    # Haz clic en el elemento
    elemento.click()
    time.sleep(4)
    # Encuentra la tabla por su ID
    tabla = driver.find_element(By.ID, "tablaStock")

    # Encuentra todos los elementos 'td' dentro de la tabla
    td_elements = tabla.find_elements(By.TAG_NAME, "td")
    # td_elements=td_elements[4:]

    for j in td_elements:
        if contador == 13:
            contador = 0
        elif contador == 6:
            productos.append(str(j.text))
            contador += 1
        else:
            contador += 1
    return productos

def eliminar_repetidos(codigos_tot,cantidades_tot,productos_tot):
    for indice, i in enumerate(codigos_tot):
        if codigos_tot.count(i) >= 2:
            codigos_tot.pop(indice)
            cantidades_tot.pop(indice)
            productos_tot.pop(indice)
    return codigos_tot, cantidades_tot, productos_tot
def ir_a_carrito_suizo(driver):
    # Itera sobre cada input para extraer su valor
    carro_qty_element = driver.find_element(By.ID, "carroqty")
    carro_qty_element.click()
    time.sleep(5)


def obtener_cantidades_suizo(driver):
    cantidades = []
    inputs_cant = driver.find_elements(By.CSS_SELECTOR, 'input.cant')
    for input_element in inputs_cant:
        value = input_element.get_attribute('value')
        cantidades.append(value)  # Imprime el valor de cada input
    return cantidades

def elegir_mas_barato(precios_sud, precios_suizo, codigos,cantidades):
    lista_sud = []
    lista_suizo = []
    cantidades_sud = []
    cantidades_suizo = []

    for i in range(len(codigos)):
        if int(precios_sud[i].replace(".","").split(",")[0]) < int(precios_suizo[i].replace(".","").split(",")[0]):
            lista_sud.append(codigos[i])
            cantidades_sud.append(cantidades[i])
        else:
            lista_suizo.append(codigos[i])
            cantidades_suizo.append(cantidades[i])
    return lista_suizo, lista_sud,cantidades_suizo,cantidades_sud

def buscar_numero_mas_de_6_digitos(cadena):
    # Patrón de expresión regular para encontrar números de 6 o más dígitos
    patron = re.compile(r'\b\d{6,}\b')
    # Buscar coincidencias en la cadena
    coincidencias = patron.findall(cadena)

    # Devolver True si se encuentra al menos una coincidencia
    return coincidencias
def eliminar_hasta_string(lista_comparacion, lista_completa):
    if lista_comparacion[0] in lista_completa:
        indice = lista_completa.index(lista_comparacion[0])
        # Elimina los elementos de la lista completa hasta el índice encontrado
        lista_ajustada = lista_completa[indice:]
    else:
        lista_ajustada = lista_completa  # O maneja este caso según necesites
    return lista_ajustada


def filtrar_elementos(td_elements):
    # Filtrar los elementos <td> que contienen "Si" o "No" como texto
    stock = []

    for td in td_elements:
        texto_td = td.text.strip()  # Obtener el texto del <td> eliminando espacios en blanco al principio y al final
        if texto_td == "Si" or texto_td == "No" or texto_td == "Pocos":
            stock.append(td.text)

    return stock

def mostrar_lista_con_salto(lista, elementos_por_linea):
    for i, elemento in enumerate(lista, start=1):
        print(elemento, end='  |  ')
        if i % elementos_por_linea == 0:
            print()

def obtener_codigo(onmouseover_content):
    cleaned_html = re.search("ddrivetip\('(.*?)',", onmouseover_content).group(1)

    # Analizar el HTML con BeautifulSoup
    soup = BeautifulSoup(cleaned_html, "html.parser")

    # Extraer
    all_text = soup.get_text()

    # Extraer el texto de las etiquetas <b> y eliminarlo del texto total
    for b_tag in soup.find_all('b'):
        all_text = all_text.replace(b_tag.get_text(), '')

    # Imprimir el texto restante (fuera de las etiquetas <b>)
    primer_elemento = all_text.split()[0]
    print("obtener codigo: "+str(primer_elemento))
    return primer_elemento

def obtener_descripcion(onmouseover_content):
    cleaned_html = re.search("ddrivetip\('(.*?)',", onmouseover_content).group(1)

    # Analizar el HTML con BeautifulSoup
    soup = BeautifulSoup(cleaned_html, "html.parser")

    # Extraer
    all_text = soup.get_text()

    # Extraer el texto de las etiquetas <b> y eliminarlo del texto total
    primer_elemento = str(all_text).split(":")
    resultado = primer_elemento[0][:-11]
    #print("obtener descripcion: " + resultado)

    return primer_elemento

def escribir(i, j, p, descripciones, codigos_de_barra, stock, precios, precios_con_descuento, precios_sugeridos):
    # Crear un nuevo libro de trabajo (workbook)
    libro = openpyxl.Workbook()

    # Seleccionar la hoja activa del libro (por defecto, hay una hoja llamada 'Sheet')
    hoja = libro.active

    # Escribir los datos en columnas (verticalmente)
    for d, c, s, p, pcd, ps in zip(descripciones, codigos_de_barra, stock, precios, precios_con_descuento,
                                   precios_sugeridos):
        hoja.append([d, c, s, p, pcd, ps])

    # Guardar el libro de trabajo en un archivo Excel
    libro.save(f'datos_{str(i)+str(j)+str(p)}.xlsx')


def quitar_caracteres(string):
    if len(string) >= 7:  # Verificar que el string tenga al menos 7 caracteres
        nuevo_string = string[3:-4]  # 3-> <b>  4-></b>
        return nuevo_string
    else:
        return "El string es demasiado corto para quitar los caracteres especificados"


def procesar_precios(lista):
    a = []
    b = []
    c = []
    contador = 0
    for i in lista:
        if contador > 11:
            contador = 0
        if contador == 8:
            a.append(i)
        elif contador == 9:
            b.append(i)
        elif contador == 11:
            c.append(i)

        contador += 1
    return a, b, c