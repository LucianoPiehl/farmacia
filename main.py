import datetime
from ExtraerCarrito import extraer_carrito_suizo, extraer_carrito_sud,\
    extraer_descripciones_suizo, extraer_descripciones_sud
from IniciarSesion import iniciar_sesion_suizo,  iniciar_sesion_sud
from RecopilarPrecios import recopilacion_precios_suizo, recopilacion_precios_sud
from auxiliar import elegir_mas_barato, eliminar_repetidos

"""
CODIGO HECHO POR LUCIANO PIEHL
27-2-2022
Este codigo podría utilizar objetos con metodos abstractos 
y sería mucho mas legible el codigo. Debido a la no continuidad del proyecto no realizo el cambio. 
Pero lo dejo asentado por si la negociacion del proyecto se retoma en un producto.
"""

#Esta lista almacena que droguerias estan disponibles en turno mañana y tarde
#en cada dia de la semana
semana = [[['SUD', 'MONROE'], ['MONROE', 'SUIZO']], [['SUD', 'MONROE', 'SUIZO'], ['SUR', 'MONROE', 'SUIZO']], [['SUD', 'MONROE', 'SUIZO'], ['SUR', 'MONROE', 'SUIZO']], [['SUD', 'MONROE', 'SUIZO'], ['SUR', 'MONROE', 'SUIZO']], [['SUD', 'MONROE', 'SUIZO'], ['SUR', 'MONROE', 'SUIZO']], [['SUD', 'MONROE', 'SUIZO'], ['MONROE']], [[], []]]

# Obtén la fecha y hora actual
now = datetime.datetime.now()
# Obtén el día de la semana como un número (0 es lunes, 6 es domingo)
dia_semana = now.weekday()

now = datetime.datetime.now()

# Iniciar Sesion
driver_sud = iniciar_sesion_sud()
driver_suizo= iniciar_sesion_suizo()

# Extraer Descripciones de los productos en los carritos de cada drogueria
driver_suizo, productos1 = extraer_descripciones_suizo(driver_suizo)
driver_sud, productos = extraer_descripciones_sud(driver_sud)

productos_tot = productos1 + productos1

# Recopilar datos de los productos extraidos en la linea 24 a 28
driver_suizo , codigos1, cantidades1 = extraer_carrito_suizo(driver_suizo, productos_tot)
driver_sud, codigos, cantidades = extraer_carrito_sud(driver_sud, productos_tot)


codigos_tot = codigos + codigos1
cantidades_tot = cantidades + cantidades1


#Eliminar repetidos
codigos_tot, cantidades_tot, productos_tot = eliminar_repetidos(codigos_tot,cantidades_tot,productos_tot)

#Buscar precios en las distintas droguerias
descripciones1, precios1 = recopilacion_precios_suizo(driver_suizo, productos_tot, codigos_tot)
descripciones2, precios2 = recopilacion_precios_sud(driver_sud, productos_tot, codigos_tot)

descripciones_tot = descripciones2 + descripciones1

#Elegir el la drogueria que conviene usar para cada producto
lista_suizo, lista_sud, cantidades_suizo, cantidades_sud = elegir_mas_barato(precios2, precios1, codigos_tot, cantidades_tot)

#Agregar a carrito
#agregar_a_carrito_suizo(driver_suizo , lista_suizo, cantidades_suizo)
#agregar_a_carrito_sud(driver, lista_sud, cantidades_sud)



