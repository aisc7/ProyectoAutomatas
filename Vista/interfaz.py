from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox)
from PySide6.QtGui import QPainter, QPen, QBrush, QColor
from PySide6.QtCore import Qt, QPointF
import pyqtgraph as pg
import sys
import math

class AutomataApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Verificador de AFD/AFND desde ER")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("background-color: #2E3440; color: white; font-size: 14px;")

        layout = QVBoxLayout()

        self.label_er = QLabel("Expresión Regular:")
        self.input_er = QLineEdit()
        self.input_er.setStyleSheet("padding: 8px; border-radius: 5px; background-color: white; color: black;")
        
        self.button_verificar = QPushButton("Generar y Verificar")
        self.button_verificar.setStyleSheet("padding: 10px; background-color: #5E81AC; color: white; border-radius: 5px;")
        self.button_verificar.clicked.connect(self.verificar_y_visualizar)
        
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setStyleSheet("background-color: white; color: black; padding: 8px; border-radius: 5px;")
        
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground("w")
        self.graph_widget.setAspectLocked(True)
        
        layout.addWidget(self.label_er)
        layout.addWidget(self.input_er)
        layout.addWidget(self.button_verificar)
        layout.addWidget(self.resultado)
        layout.addWidget(self.graph_widget)
        self.setLayout(layout)

    def verificar_y_visualizar(self):
        try:
            regex = self.input_er.text()
            # Simulación de estructura de un autómata (debes reemplazarlo con tu lógica real)
            automata = {
                "estados": ["q0", "q1", "q2"],
                "transiciones": {("q0", "a"): "q1", ("q1", "b"): "q2"},
                "estado_inicial": "q0",
                "estados_aceptacion": ["q2"]
            }
            self.resultado.setText("El autómata generado es un AFND.")
            self.dibujar_automata(automata)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al procesar la expresión regular: {str(e)}")

    def dibujar_automata(self, automata):
        self.graph_widget.clear()
        estados = automata["estados"]
        transiciones = automata["transiciones"]
        estado_inicial = automata["estado_inicial"]
        estados_aceptacion = automata["estados_aceptacion"]

        radio = 150
        centro_x, centro_y = 0, 0
        angulo_paso = 2 * math.pi / len(estados)
        posiciones_estados = {}

        for i, estado in enumerate(estados):
            x = centro_x + radio * math.cos(i * angulo_paso)
            y = centro_y + radio * math.sin(i * angulo_paso)
            posiciones_estados[estado] = (x, y)

            circulo = pg.QtWidgets.QGraphicsEllipseItem(x - 20, y - 20, 40, 40)
            circulo.setPen(QPen(Qt.black, 2))
            if estado in estados_aceptacion:
                circulo.setBrush(QBrush(QColor(255, 200, 200)))
            self.graph_widget.addItem(circulo)

            texto = pg.TextItem(estado, anchor=(0.5, 0.5))
            texto.setPos(x, y)
            self.graph_widget.addItem(texto)

            if estado == estado_inicial:
                flecha = pg.ArrowItem(pos=(x - 40, y), angle=0, tipAngle=30, headLen=20, tailLen=10, pen=QPen(Qt.black, 2))
                self.graph_widget.addItem(flecha)

        for (estado_inicio, simbolo), estado_destino in transiciones.items():
            x1, y1 = posiciones_estados[estado_inicio]
            x2, y2 = posiciones_estados[estado_destino]
            
            angulo = math.degrees(math.atan2(y2 - y1, x2 - x1))
            flecha = pg.ArrowItem(pos=(x2, y2), angle=angulo, tipAngle=30, headLen=20, tailLen=10, pen=QPen(Qt.black, 2))
            self.graph_widget.addItem(flecha)

            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            texto = pg.TextItem(simbolo, anchor=(0.5, 0.5))
            texto.setPos(mid_x, mid_y)
            self.graph_widget.addItem(texto)

