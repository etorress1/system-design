"""Ejercicio 1: un value object y una entidad de ReservaU.

- FranjaHoraria: una franja de una cancha en un dia, de la hora inicio a
  la hora fin (fin no incluida: de 18 a 19 es una hora). Dos franjas con
  los mismos datos son la misma franja.
- Reserva: una reserva concreta, con su id. Dos reservas con el mismo id
  son la misma reserva, aunque se haya movido a otra franja.

Corre esto para ver el resultado:

    python3 franja_ejercicio1.py

Y las pruebas con:

    pytest test_franja_ejercicio1.py
"""

from dataclasses import dataclass

HORA_DE_APERTURA = 7
HORA_DE_CIERRE = 21


@dataclass(frozen=True)
class FranjaHoraria:
    fecha: str
    inicio: int
    fin: int

    def __post_init__(self):
        if self.inicio >= self.fin or self.inicio < HORA_DE_APERTURA or self.fin > HORA_DE_CIERRE:
            raise ValueError("franja invalida")

    def duracion(self):
        return self.fin - self.inicio

    def se_solapa_con(self, otra):
        return self.fecha == otra.fecha and self.inicio < otra.fin and otra.inicio < self.fin


class Reserva:
    def __init__(self, id_reserva, estudiante, franja):
        self.id = id_reserva
        self.estudiante = estudiante
        self.franja = franja

    def __eq__(self, otra):
        if not isinstance(otra, Reserva):
            return NotImplemented
        return self.id == otra.id

    def __hash__(self):
        return hash(self.id)