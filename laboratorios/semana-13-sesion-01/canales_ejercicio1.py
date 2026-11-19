
from calendario_eventos import CalendarioConEventos, ObservadorDeReservas
from conexiones import ConexionSimulada


def tema_de(cancha, fecha):
    return cancha + "/" + fecha


class Canales:
    def __init__(self):
        self.suscritos = {}

    def suscribir(self, tema, conexion):
        if tema not in self.suscritos:
            self.suscritos[tema] = []

        if conexion not in self.suscritos[tema]:
            self.suscritos[tema].append(conexion)

    def desuscribir(self, tema, conexion):
        if conexion in self.suscritos.get(tema, []):
            self.suscritos[tema].remove(conexion)

    def suscriptores(self, tema):
        return len(self.suscritos.get(tema, []))

    def publicar(self, tema, mensaje):
        entregados = 0

        for conexion in self.suscritos.get(tema, []):
            if conexion.enviar(mensaje):
                entregados += 1

        return entregados


class PublicadorDeDisponibilidad(ObservadorDeReservas):
    def __init__(self, canales, fecha):
        self.canales = canales
        self.fecha = fecha
        self.ultimos_entregados = 0

    def al_ocuparse(self, cancha, franja):
        mensaje = f"ocupada {franja.inicio}-{franja.fin}"
        tema = tema_de(cancha, franja.fecha)

        self.ultimos_entregados = self.canales.publicar(
            tema, mensaje
        )

    def al_liberarse(self, cancha, franja):
        mensaje = f"liberada {franja.inicio}-{franja.fin}"
        tema = tema_de(cancha, franja.fecha)

        self.ultimos_entregados = self.canales.publicar(
            tema, mensaje
        )

