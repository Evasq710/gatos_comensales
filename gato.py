import time
import random
import threading

AMARILLO = '\033[93m'
VERDE = '\033[92m'
RESET = '\033[0m'

class Gato(threading.Thread):
    def __init__(self, id, nombre, bocados_para_saciarse, tenedor_izq: threading.Lock, tenedor_der: threading.Lock, tiempo_asignado, flag_actualizacion: threading.Event):
        super().__init__()
        self.id = id
        self.nombre = nombre
        self.bocados_para_saciarse = bocados_para_saciarse
        self.tenedor_izq = tenedor_izq
        self.tenedor_der = tenedor_der
        self.tiempo_asignado = tiempo_asignado
        self.estado = 0  # 0 = pensando, 1 = hambriento, 2 = comiendo, 3 = saciado
        self.descripcion_estado = ""
        self.flag_actualizacion = flag_actualizacion

    def run(self):
        while self.bocados_para_saciarse > 0:
            self.pensando()
            time.sleep(random.randint(3, 4))

            self.hambriento()
            time.sleep(1)
            # Los gatos con ID par toman primero el tenedor izquierdo
            # Los gatos con ID impar toman primero el tenedor derecho
            if self.id % 2 == 0:
                primer_tenedor, segundo_tenedor = self.tenedor_izq, self.tenedor_der
            else:
                primer_tenedor, segundo_tenedor = self.tenedor_der, self.tenedor_izq

            primer_tenedor.acquire()
            segundo_tenedor.acquire()
            for _ in range(self.tiempo_asignado):
                if self.bocados_para_saciarse == 0:
                    break
                self.comer()
                time.sleep(random.randint(3, 5))
            segundo_tenedor.release()
            primer_tenedor.release()

        self.pensando()  # Último estado pensando (saciado)
    
    def pensando(self):
        self.estado = 0 if self.bocados_para_saciarse > 0 else 3
        self.descripcion_estado = f"[G{self.id}] {self.nombre} está PENSANDO..." if self.estado == 0 else f"[G{self.id}] {self.nombre} está SACIADO!!!"
        self.flag_actualizacion.set()
    
    def hambriento(self):
        self.estado = 1
        self.descripcion_estado = f"[G{self.id}] {self.nombre} está HAMBRIENTO..."
        self.flag_actualizacion.set()

    def comer(self):
        self.estado = 2
        self.bocados_para_saciarse -= 1
        self.descripcion_estado = f"[G{self.id}] {self.nombre} está COMIENDO..."
        self.flag_actualizacion.set()

    def retornar_lineas_gato(self):
        espacios = ' ' * 25 if self.id == 1 \
              else ' ' * 22 if self.id == 2 \
              else ' ' * 10 if self.id == 3 \
              else ' ' *  5 if self.id == 4 \
              else ''
        
        tenedor = f'Ten.1: {"*" if self.tenedor_izq.locked() else "-"} {' '*10} Ten.2: {"*" if self.tenedor_der.locked() else "-"}' if self.id == 1 \
             else f'Ten.3: {"*" if self.tenedor_der.locked() else "-"} {' '*10}' if self.id == 2 \
             else f'         {' '*20} Ten.4: {"*" if self.tenedor_izq.locked() else "-"}' if self.id == 4 \
             else f'         {' '*10} Ten.5: {"*" if self.tenedor_izq.locked() else "-"}' if self.id == 5 \
             else  ''

        if self.estado == 0: # pensando
            lineas = f'''
{espacios}{RESET}== {self.nombre} [{self.id}] está PENSANDO ==
{espacios}{RESET}                            
{espacios}{RESET}    |\\__/,|   (`\\           
{espacios}{RESET}  _.|o o  |_   ) )          
{espacios}{RESET}-(((---(((--------          
{espacios}{RESET}{self.bocados_para_saciarse} bocados para estar saciado
{espacios}{RESET}                            
{espacios}{RESET}{tenedor}'''
        elif self.estado == 1: # hambriento
            lineas = f'''
{espacios}{AMARILLO}== {self.nombre} [{self.id}] está HAMBRIENTO ==
{espacios}{AMARILLO}                            
{espacios}{AMARILLO}    |\\__/,|   (`\\           
{espacios}{AMARILLO}  _.|o o  |_   ) )          
{espacios}{AMARILLO}-(((---(((--------          
{espacios}{RESET}{self.bocados_para_saciarse} bocados para estar saciado
{espacios}{RESET}                            
{espacios}{RESET}{tenedor}'''
        elif self.estado == 2: # comiendo
            lineas = f'''
{espacios}{VERDE}== {self.nombre} [{self.id}] está COMIENDO ==
{espacios}{VERDE} _._     _,-'""`-._           
{espacios}{VERDE}(,-.`._,'(       |\\`-/|       
{espacios}{VERDE}    `-.-' \\ )-`( , o o)       
{espacios}{VERDE}          `-    \\`_`"'-       
{espacios}{RESET}{self.bocados_para_saciarse} bocados para estar saciado
{espacios}{RESET}                            
{espacios}{RESET}{tenedor}'''
        else: # saciado
            lineas = f'''
{espacios}{RESET}== {self.nombre} [{self.id}] está SACIADO ==
{espacios}{RESET}      |\\      _,,,---,,_      
{espacios}{RESET}ZZZzz /,`.-'`'    -.  ;-;;,_  
{espacios}{RESET}     |,4-  ) )-,_. ,\\ (  `'-' 
{espacios}{RESET}    '---''(_/--'  `-'\\_)      
{espacios}{RESET}                            
{espacios}{RESET}                            
{espacios}{RESET}{tenedor}'''
            
        return lineas.split('\n')