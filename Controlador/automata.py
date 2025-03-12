
class Automata:
    def __init__(self, estados, alfabeto, transiciones, estado_inicial, estados_aceptacion):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion

    def es_afd(self):
        for estado in self.estados:
            for simbolo in self.alfabeto:
                # Verificar si hay más de una transición para el mismo símbolo
                if len(self.transiciones.get((estado, simbolo), [])) != 1:
                    return False
        return True

    def es_afnd(self):
        return not self.es_afd()