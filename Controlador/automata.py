import re

class Automata:
    def __init__(self, regex):
        self.regex = regex
        self.estados, self.alfabeto, self.transiciones, self.estado_inicial, self.estados_aceptacion = self.convertir_er_a_afn()

    def convertir_er_a_afn(self):
        # Simulación de conversión de ER a AFN (Ejemplo simple, debe mejorarse)
        estados = ["q0", "q1"]
        alfabeto = list(set(re.findall(r'[a-z]', self.regex)))
        transiciones = {("q0", simbolo): ["q1"] for simbolo in alfabeto}
        estado_inicial = "q0"
        estados_aceptacion = ["q1"]
        return estados, alfabeto, transiciones, estado_inicial, estados_aceptacion

    def es_afd(self):
        for estado in self.estados:
            for simbolo in self.alfabeto:
                if len(self.transiciones.get((estado, simbolo), [])) != 1:
                    return False
        return True