
import os
import random
import threading
from gato import Gato

todos_saciados = False
actualizar_consola = threading.Event()

tenedores = [threading.Lock() for _ in range(5)]
nombres = ["Michi", "Garfield", "Misifus", "Felix", "Tom"]
gatos = [
    Gato(
        id=i+1,
        nombre=nombres[i],
        bocados_para_saciarse=random.randint(5, 10),
        tenedor_izq=tenedores[i],
        tenedor_der=tenedores[(i+1)%5],
        tiempo_asignado=2,
        flag_actualizacion=actualizar_consola
    ) for i in range(5)
]

actualizaciones = 0
def mostrar_gatos():
    global gatos, actualizaciones, todos_saciados

    while not todos_saciados:
        if all(gato.estado == 3 for gato in gatos):
            break
        
        # Esperando a que un gato actualice su estado
        actualizar_consola.wait()
        actualizar_consola.clear()

        # Limpiando terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        actualizaciones += 1
        print(f"Actualización: {actualizaciones}\n")
        
        # Mostrando estado de los gatos
        for linea in gatos[0].retornar_lineas_gato():
            print(linea)
        for linea1, linea2 in zip(gatos[4].retornar_lineas_gato(), gatos[1].retornar_lineas_gato()):
            print(linea1 + linea2)
        for linea1, linea2 in zip(gatos[3].retornar_lineas_gato(), gatos[2].retornar_lineas_gato()):
            print(linea1 + linea2)
        
        print()
        for gato in gatos:
            print(gato.descripcion_estado)
        print()



for gato in gatos:
    gato.start()

mostrar_gatos()

for gato in gatos:
    gato.join()

print("\nTodos los gatos están saciados. ¡Fin del programa!")

