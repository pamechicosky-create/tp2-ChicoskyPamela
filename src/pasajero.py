GRUPOS_EDAD = ("nino", "adolescente", "adulto", "mayor", "desconocida")


class Pasajero:
    def __init__(self, id_pasajero, nombre, billete, clase, edad, sobrevivio):
        self.id = id_pasajero
        self.nombre = nombre
        self.billete = billete
        self.clase = clase
        self.edad = edad
        self.sobrevivio = sobrevivio

    def grupo_edad(self):
        if self.edad is None:
            return "desconocida"
        if self.edad <= 12:
            return "nino"
        if self.edad <= 17:
            return "adolescente"
        if self.edad <= 59:
            return "adulto"
        return "mayor"

    def a_ficha(self):
        return {
            "PassengerId": self.id,
            "Nombre": self.nombre,
            "Billete": self.billete,
            "Clase": self.clase,
            "Edad": "" if self.edad is None else self.edad,
            "GrupoEdad": self.grupo_edad(),
            "Sobrevivio": "Sí" if self.sobrevivio else "No",
        }

    def __repr__(self):
        return f"Pasajero({self.id}, {self.nombre!r})"
