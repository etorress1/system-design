"""Ejercicio 2: invalidar el cache al reservar, y darle a cada entrada un
tiempo de vida (TTL).

Corre las pruebas con:

    pytest test_invalidacion_ttl_ejercicio2.py

No cambies los nombres de la clase ni de los metodos: los tests
dependen de que existan exactamente asi.
"""


class ServicioConInvalidacionYTTL:
    def __init__(self, repositorio, reloj, ttl):
        self.repositorio = repositorio
        self.reloj = reloj
        self.ttl = ttl
        self.cache = {}
        self.aciertos = 0
        self.fallos = 0

    def disponibilidad(self, cancha, fecha):
        clave = (cancha, fecha)
        ahora = self.reloj.ahora()

        entrada = self.cache.get(clave)
        if entrada is not None:
            libres, guardado_en = entrada
           
            if ahora - guardado_en < self.ttl:
                self.aciertos += 1
                return libres

        # Fallo: no existe o ya vencio
        self.fallos += 1
        libres = self.repositorio.horas_libres(cancha, fecha)  
        self.cache[clave] = (libres, ahora)  
        return libres

    def reservar(self, cancha, fecha, hora):
    
        libres = self.repositorio.horas_libres(cancha, fecha)  
        if hora not in libres:
            return False

        self.repositorio.registrar_reserva(cancha, fecha, hora)
       
        self.cache.pop((cancha, fecha), None)
        return True