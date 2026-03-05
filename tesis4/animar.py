from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PySide6.QtCore import QPropertyAnimation, QRect, Qt

class PHAnimado(QFrame):
    """
    Esta clase representa la tarjeta de pH con animación de barra.
    Se puede integrar en cualquier GUI principal.
    """
    def __init__(self, titulo="pH", ancho=50, alto=150):
        super().__init__()
        self.setStyleSheet("""
            background-color: #f9fafb;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 5px;
        """)

        self.layout = QVBoxLayout(self)

        # Título
        self.label_titulo = QLabel(titulo)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_titulo)

        # Valor numérico
        self.label_valor = QLabel("—")
        self.label_valor.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_valor)

        # Contenedor de barra
        self.ph_contenedor = QFrame()
        self.ph_contenedor.setFixedSize(ancho, alto)
        self.ph_contenedor.setStyleSheet("background-color: #e5e7eb; border-radius: 5px;")
        self.layout.addWidget(self.ph_contenedor, alignment=Qt.AlignCenter)

        # Barra animada
        self.barra_ph = QFrame(self.ph_contenedor)
        self.barra_ph.setGeometry(0, alto, ancho, 0)
        self.barra_ph.setStyleSheet("background-color: #10b981; border-radius: 5px;")

    def actualizar_ph(self, valor):
        """Actualiza valor y animación de la barra"""
        try:
            valor = float(valor)
        except:
            return
        if valor < 0: valor = 0
        if valor > 14: valor = 14

        self.label_valor.setText(f"{valor:.1f}")

        altura = int((valor / 14) * self.ph_contenedor.height())
        nueva_y = self.ph_contenedor.height() - altura

        anim = QPropertyAnimation(self.barra_ph, b"geometry")
        anim.setDuration(500)
        anim.setStartValue(self.barra_ph.geometry())
        anim.setEndValue(QRect(0, nueva_y, self.ph_contenedor.width(), altura))
        anim.start()
