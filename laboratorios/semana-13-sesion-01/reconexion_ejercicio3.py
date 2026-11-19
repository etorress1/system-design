from canales_ejercicio1 import Canales


class CanalConHistorial(Canales):
    def __init__(self, historial=50):
        super().__init__()
        self.historial = historial
        self.numeros = {}
        self.mensajes = {}

    def publicar(self, tema, mensaje):
        if tema not in self.numeros:
            self.numeros[tema] = 0
            self.mensajes[tema] = []

        self.numeros[tema] += 1
        numero = self.numeros[tema]

        texto = f"{numero} {mensaje}"

        self.mensajes[tema].append((numero, texto))

        if len(self.mensajes[tema]) > self.historial:
            self.mensajes[tema].pop(0)

        for conexion in self.suscritos.get(tema, []):
            conexion.enviar(texto)

        return numero

    def ultimo_numero(self, tema):
        return self.numeros.get(tema, 0)

    def reconectar(self, tema, conexion, ultimo_visto):
        ultimo = self.ultimo_numero(tema)

        if ultimo_visto > ultimo:
            raise ValueError("numero desconocido")

        historial = self.mensajes.get(tema, [])

        if ultimo_visto < ultimo:
            if not historial or ultimo_visto < historial[0][0] - 1:
                conexion.enviar("recargar")
            else:
                for numero, mensaje in historial:
                    if numero > ultimo_visto:
                        conexion.enviar(mensaje)

        self.suscribir(tema, conexion)
