import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QBrush, QColor
import pyqtgraph as pg
from pyqtgraph import ArrowItem
from Controlador.automata import Automata


class VisualizadorAutomata(QWidget):
    def __init__(self, estados, transiciones, estado_inicial, estados_aceptacion):
        super().__init__()
        self.estados = estados
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Visualizador de Autómata")
        self.setGeometry(100, 100, 800, 600)

        # Crear un widget de gráficos
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground("w")
        self.graph_widget.setAspectLocked(True)

        # Dibujar el autómata
        self.dibujar_automata()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.graph_widget)
        self.setLayout(layout)

    def dibujar_automata(self):
        # Configurar las posiciones de los estados en un círculo
        radio = 200
        centro = QPointF(0, 0)
        angulo_paso = 360 / len(self.estados)
        posiciones_estados = {}

        for i, estado in enumerate(self.estados):
            angulo = i * angulo_paso
            x = centro.x() + radio * pg.math.cosd(angulo)
            y = centro.y() + radio * pg.math.sind(angulo)
            posiciones_estados[estado] = (x, y)

            # Dibujar el estado como un círculo
            circulo = pg.QtWidgets.QGraphicsEllipseItem(x - 20, y - 20, 40, 40)
            circulo.setPen(QPen(Qt.black, 2))
            if estado in self.estados_aceptacion:
                circulo.setBrush(QBrush(QColor(255, 200, 200)))  # Color para estados de aceptación
            self.graph_widget.addItem(circulo)

            # Etiquetar el estado
            texto = pg.TextItem(estado, anchor=(0.5, 0.5))
            texto.setPos(x, y)
            self.graph_widget.addItem(texto)

            # Dibujar una flecha para el estado inicial
            if estado == self.estado_inicial:
                flecha = ArrowItem(
                    pos=(x - 40, y),
                    angle=angulo + 90,
                    tipAngle=30,
                    headLen=20,
                    tailLen=10,
                    pen=QPen(Qt.black, 2),
                )
                self.graph_widget.addItem(flecha)

        # Dibujar las transiciones
        for (estado_inicio, simbolo), estados_destino in self.transiciones.items():
            for estado_destino in estados_destino:
                x1, y1 = posiciones_estados[estado_inicio]
                x2, y2 = posiciones_estados[estado_destino]

                # Dibujar una flecha entre los estados
                flecha = ArrowItem(
                    pos=(x2, y2),
                    angle=pg.math.degrees(pg.math.atan2(y2 - y1, x2 - x1)),
                    tipAngle=30,
                    headLen=20,
                    tailLen=10,
                    pen=QPen(Qt.black, 2),
                )
                self.graph_widget.addItem(flecha)

                # Etiquetar la transición con el símbolo
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                texto = pg.TextItem(simbolo, anchor=(0.5, 0.5))
                texto.setPos(mid_x, mid_y)
                self.graph_widget.addItem(texto)


class AutomataApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Verificador de AFD/AFND")

        layout = QVBoxLayout()

        # Campos de entrada
        self.label_estados = QLabel("Estados (separados por coma):")
        self.input_estados = QLineEdit()

        self.label_alfabeto = QLabel("Alfabeto (separados por coma):")
        self.input_alfabeto = QLineEdit()

        self.label_transiciones = QLabel(
            "Transiciones (formato: estado,símbolo,estado_destino; separadas por coma):"
        )
        self.input_transiciones = QLineEdit()

        self.label_estado_inicial = QLabel("Estado inicial:")
        self.input_estado_inicial = QLineEdit()

        self.label_estados_aceptacion = QLabel("Estados de aceptación (separados por coma):")
        self.input_estados_aceptacion = QLineEdit()

        # Botón para verificar y visualizar
        self.button_verificar = QPushButton("Verificar y Visualizar")
        self.button_verificar.clicked.connect(self.verificar_y_visualizar)

        # Área de resultados
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)

        # Agregar widgets al layout
        layout.addWidget(self.label_estados)
        layout.addWidget(self.input_estados)
        layout.addWidget(self.label_alfabeto)
        layout.addWidget(self.input_alfabeto)
        layout.addWidget(self.label_transiciones)
        layout.addWidget(self.input_transiciones)
        layout.addWidget(self.label_estado_inicial)
        layout.addWidget(self.input_estado_inicial)
        layout.addWidget(self.label_estados_aceptacion)
        layout.addWidget(self.input_estados_aceptacion)
        layout.addWidget(self.button_verificar)
        layout.addWidget(self.resultado)

        self.setLayout(layout)

    def verificar_y_visualizar(self):
        try:
            # Obtener los datos de la interfaz
            estados = self.input_estados.text().split(",")
            alfabeto = self.input_alfabeto.text().split(",")
            transiciones_raw = self.input_transiciones.text().split(";")
            estado_inicial = self.input_estado_inicial.text()
            estados_aceptacion = self.input_estados_aceptacion.text().split(",")

            # Procesar las transiciones
            transiciones = {}
            for trans in transiciones_raw:
                estado_inicio, simbolo, estado_destino = trans.split(",")
                if (estado_inicio, simbolo) not in transiciones:
                    transiciones[(estado_inicio, simbolo)] = []
                transiciones[(estado_inicio, simbolo)].append(estado_destino)

            # Crear el autómata
            automata = Automata(estados, alfabeto, transiciones, estado_inicial, estados_aceptacion)

            # Verificar si es AFD o AFND
            if automata.es_afd():
                self.resultado.setText("El autómata es un AFD.")
            else:
                self.resultado.setText("El autómata es un AFND.")

            # Mostrar la visualización
            self.visualizador = VisualizadorAutomata(estados, transiciones, estado_inicial, estados_aceptacion)
            self.visualizador.show()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al procesar el autómata: {str(e)}")


