from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout
from PySide6.QtCore import QTimer, Qt

class WaterLevelCard(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: #f2f4f7; border-radius:12px; border:1px solid #d0d3da;")
        self.setFixedSize(100, 150)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5,5,5,5)
        self.layout.addStretch()

        # Nivel de agua real
        self.water = QFrame(self)
        self.water.setStyleSheet("background: #3b82f6; border-radius:8px;")
        self.water.setFixedHeight(0)  # inicial vacío
        self.water.setMaximumWidth(self.width()-10)
        self.layout.addWidget(self.water)

        self.level = 0  # nivel actual 0-100

    def set_level(self, level_percent):
        """Actualizar el nivel de agua animando la altura"""
        self.level = max(0, min(100, level_percent))
        height = int(self.height() * (self.level / 100))
        self.water.setFixedHeight(height)


import random
class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nivel de Agua Animado")
        self.resize(200,200)

        self.layout = QHBoxLayout(self)
        self.card = WaterLevelCard()
        self.layout.addWidget(self.card)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_level)
        self.timer.start(1000)  # cada 1 segundo

    def update_level(self):
        # Simula que el nivel baja o sube
        nivel = random.randint(0,100)
        self.card.set_level(nivel)

if __name__ == "__main__":
    app = QApplication([])
    demo = Demo()
    demo.show()
    app.exec()
