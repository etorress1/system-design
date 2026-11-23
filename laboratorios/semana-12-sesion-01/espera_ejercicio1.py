"""Ejercicio 1: la lista de espera, primero consultando y despues con
Observer.
"""

from notificaciones import NotificadorEnMemoria
from reservas import CalendarioDeCancha, FranjaHoraria

SEGUNDO_DE_LA_CANCELACION = 5500


# ---------------------------------------------------------------- Parte A

def simular_consultas(intervalo_segundos):
    calendario = CalendarioDeCancha("cancha-1", "2026-11-10")
    calendario.reservar("r-1", "ana", 18, 19)
    consultas = 0
    segundo = 0

    while True:
        if segundo >= SEGUNDO_DE_LA_CANCELACION and not calendario.esta_libre(18, 19):
            calendario.cancelar("r-1")

        consultas = consultas + 1

        if calendario.esta_libre(18, 19):
            return consultas, segundo

        segundo = segundo + intervalo_segundos


# ---------------------------------------------------------------- Parte B

class ObservadorDeCalendario:
    """Contrato que deben implementar los observadores."""

    def al_liberarse(self, cancha, franja):
        raise NotImplementedError


class CalendarioObservable(CalendarioDeCancha):

    def __init__(self, cancha, fecha):
        super().__init__(cancha, fecha)
        self.observadores = []

    def suscribir(self, observador):
        self.observadores.append(observador)

    def cancelar(self, id_reserva):
        franja = self.franja_de(id_reserva)

        super().cancelar(id_reserva)

        for observador in self.observadores:
            observador.al_liberarse(self.cancha, franja)


class ListaDeEspera(ObservadorDeCalendario):

    def __init__(self, notificador):
        self.notificador = notificador
        self.esperando = {}

    def anotar(self, estudiante, franja):
        if franja not in self.esperando:
            self.esperando[franja] = []

        self.esperando[franja].append(estudiante)

    def al_liberarse(self, cancha, franja):
        if franja not in self.esperando or not self.esperando[franja]:
            return

        estudiante = self.esperando[franja].pop(0)

        texto = (
            f"Se libero {cancha} el {franja.fecha} "
            f"de {franja.inicio} a {franja.fin}"
        )

        self.notificador.enviar(estudiante, texto)


# ---------------------------------------------------------------- Ejecucion

if __name__ == "__main__":
    print("Parte A: consultando")

    for intervalo in [30, 300]:
        consultas, segundo = simular_consultas(intervalo)
        print(
            "  Cada", intervalo, "s: beto se entera en el segundo",
            segundo, "despues de", consultas, "consultas"
        )

    consultas, segundo = simular_consultas(30)

    print(
        "  2000 estudiantes esperando, cada 30 s:",
        2000 * consultas, "consultas"
    )

    print("Parte B: con Observer")

    notificador = NotificadorEnMemoria()
    lista = ListaDeEspera(notificador)

    calendario = CalendarioObservable("cancha-1", "2026-11-10")
    calendario.suscribir(lista)

    calendario.reservar("r-1", "ana", 18, 19)
    calendario.reservar("r-2", "carla", 9, 10)

    lista.anotar("beto", FranjaHoraria("2026-11-10", 18, 19))
    lista.anotar("dani", FranjaHoraria("2026-11-10", 18, 19))

    calendario.cancelar("r-2")
    calendario.cancelar("r-1")

    for destinatario, texto in notificador.enviados:
        print(" ", destinatario, "<-", texto)

    print(
        "  Siguen esperando 18-19:",
        lista.esperando[FranjaHoraria("2026-11-10", 18, 19)]
    )