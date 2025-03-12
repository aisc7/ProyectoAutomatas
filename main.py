import sys
from PySide6.QtWidgets import QApplication
from Vista.interfaz import AutomataApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AutomataApp()
    ex.show()
    sys.exit(app.exec())