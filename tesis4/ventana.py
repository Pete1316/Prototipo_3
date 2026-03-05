from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QTextEdit, QFrame
)
from PySide6.QtCore import QThread, Signal, Qt
import serial
import serial.tools.list_ports
import sys
from animar import PHAnimado

# --------------------------- HILO SERIAL ---------------------------
class ConexionSerial(QThread):
    datos_arduino = Signal(str)
    estado_conexion = Signal(str)

    def __init__(self, puerto, velocidad=9600):
        super().__init__()
        self.puerto = puerto
        self.velocidad = velocidad
        self.hilo_activo = True
        self.serial_port = None

    def run(self):
        while self.hilo_activo:
            if self.serial_port is None:
                try:
                    self.serial_port = serial.Serial(self.puerto, self.velocidad, timeout=1)
                    self.estado_conexion.emit(f"Conectado a {self.puerto}")
                except Exception as e:
                    self.estado_conexion.emit(f"No conectado: {e}")
                    self.msleep(2000)
                    continue

            try:
                linea = self.serial_port.readline().decode(errors="ignore").strip()
                if linea:
                    self.datos_arduino.emit(linea)
            except Exception as e:
                self.estado_conexion.emit(f"Error lectura: {e}")
                if self.serial_port:
                    self.serial_port.close()
                self.serial_port = None
                self.msleep(1000)

    def detener_hilo(self):
        self.hilo_activo = False
        if self.serial_port:
            try:
                self.serial_port.close()
            except:
                pass
        self.wait()

# --------------------------- VENTANA PRINCIPAL ---------------------------
class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hidroponia")
        self.setFixedSize(850, 500)
        self.hilo_serial = None

        self.agregar_cosas()
        self.refrescar_puertos()

    # --------------------------- CREAR TARJETAS ---------------------------
    def crear_tarjeta(self, titulo):
        frame = QFrame()
        frame.setStyleSheet("""
            background-color: #f9fafb;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 5px;
        """)
        layout = QVBoxLayout(frame)

        label_titulo = QLabel(titulo)
        label_titulo.setAlignment(Qt.AlignCenter)
        label_titulo.setStyleSheet("font-weight: bold; font-size: 16px;")

        label_valor = QLabel("—")
        label_valor.setAlignment(Qt.AlignCenter)
        label_valor.setStyleSheet("font-size: 24px; font-weight: bold;")

        barra_ph = QFrame()
        barra_ph.setFixedSize(80,150)
        barra_ph.setStyleSheet("background-color: #e5e7eb; border-radius: 5px;")
        
        

        layout.addWidget(label_titulo)
        layout.addWidget(label_valor)
        layout.addWidget(barra_ph, alignment=Qt.AlignCenter)

        frame.label_valor = label_valor  # Guardar referencia al valor
        return frame
    
    def crear_tarjeta_ph_animada(self, titulo="pHkk"):
        frame_1 =QFrame()
        frame_1.setStyleSheet("""
        background-color: #f9fafb;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 5px;""")
        
        layout = QVBoxLayout(frame_1)

        #Para agregar Titulo al pH
        titulo_ph = QLabel(titulo)
        titulo_ph.setAlignment(Qt.AlignCenter)
        titulo_ph.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(titulo_ph)

        return frame_1


    # --------------------------- INTERFAZ ---------------------------
    def agregar_cosas(self):
        frame = QFrame()
        frame.setStyleSheet("""
            background: #ffffff;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
        """)
        contenedor_1 = QHBoxLayout(frame)

        # ComboBox de puertos
        contenedor_1.addWidget(QLabel("Puerto"))
        self.port_combo = QComboBox()
        contenedor_1.addWidget(self.port_combo)

        # Botones de conexión
        self.refresh_btn = QPushButton("Refrescar")
        contenedor_1.addWidget(self.refresh_btn)
        self.refresh_btn.clicked.connect(self.refrescar_puertos)

        self.connect_btn = QPushButton("Conectar")
        contenedor_1.addWidget(self.connect_btn)
        self.connect_btn.clicked.connect(self.conectar_serial)

        self.disconnect_btn = QPushButton("Desconectar")
        self.disconnect_btn.setEnabled(False)
        contenedor_1.addWidget(self.disconnect_btn)
        self.disconnect_btn.clicked.connect(self.desconectar_serial)

        # Label de estado
        self.status_label = QLabel("Estado: No conectado")
        contenedor_1.addWidget(self.status_label)

        # Tarjetas de datos
        
        self.tarjeta_ph = self.crear_tarjeta("pH")
        self.tarjeta_temp = self.crear_tarjeta("Temperatura")
        self.tarjeta_hum = self.crear_tarjeta("Humedad")
        self.tarjeta_nivel = self.crear_tarjeta("Nivel Agua")

        layout_tarjetas = QHBoxLayout()
        layout_tarjetas.addWidget(self.tarjeta_ph)
        layout_tarjetas.addWidget(self.tarjeta_temp)
        layout_tarjetas.addWidget(self.tarjeta_hum)
        layout_tarjetas.addWidget(self.tarjeta_nivel)

        # QTextEdit para mostrar todos los datos
        self.texto_datos = QTextEdit()
        self.texto_datos.setReadOnly(True)
        self.texto_datos.setStyleSheet("""
            background-color: #f9fafb;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            font-family: Consolas, monospace;
            font-size: 14px;
            padding: 5px;
        """)

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(frame)
        main_layout.addLayout(layout_tarjetas)
        main_layout.addWidget(self.texto_datos)

    # --------------------------- EXTRACCIÓN DE DATOS ---------------------------
    def extraer_datos(self, linea:str):
        datos = {}
        if not linea:
            return None
        linea = linea.strip()
        if linea.startswith("pH"):
            try:
                datos['pH'] = float(linea.split(":")[1])
            except:
                datos['pH'] = None

        elif linea.startswith("Tem_AB"):
            try:
                datos['Tem_AB'] = float(linea.split(":")[1])      
            except:
                datos['Tem_AB'] = None

        elif linea.startswith("hum_AB"):
            try:
                 datos['hum_AB'] = float(linea.split(":")[1]) 
            except:
                datos['hum_AB'] = None

        elif linea.startswith("Nivel_A"):
            try:
                datos['Nivel_A'] = linea.split(":")[1].strip()

            except:
                datos['Nivel_A'] = None
            
        return datos if datos else None

    # --------------------------- MOSTRAR DATOS ---------------------------
    def mostrar_datos(self, datos):
        self.texto_datos.append(datos)
        info = self.extraer_datos(datos)
        if info:
            if 'pH' in info:
                self.tarjeta_ph.label_valor.setText(str(info['pH']))
            if 'Tem_AB' in info:
                self.tarjeta_temp.label_valor.setText(str(info['Tem_AB']))
            if 'hum_AB' in info:
                self.tarjeta_hum.label_valor.setText(str(info['hum_AB']))
            if 'Nivel_A' in info:
                self.tarjeta_nivel.label_valor.setText(str(info['Nivel_A']))

    # --------------------------- FUNCIONES DE SERIAL ---------------------------
    def refrescar_puertos(self):
        self.port_combo.clear()
        puertos = serial.tools.list_ports.comports()
        if not puertos:
            self.port_combo.addItem("No hay puertos")
            return
        for p in puertos:
            self.port_combo.addItem(p.device)

    def conectar_serial(self):
        puerto = self.port_combo.currentText()
        if not puerto or puerto == "No hay puertos":
            return
        if not self.hilo_serial:
            self.hilo_serial = ConexionSerial(puerto)
            self.hilo_serial.datos_arduino.connect(self.mostrar_datos)
            self.hilo_serial.estado_conexion.connect(self.actualizar_estado)
            self.hilo_serial.start()
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)

    def desconectar_serial(self):
        if self.hilo_serial:
            self.hilo_serial.detener_hilo()
            self.hilo_serial = None
        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)
        self.status_label.setText("Estado: No conectado")

    def actualizar_estado(self, estado):
        self.status_label.setText(f"Estado: {estado}")


# --------------------------- MAIN ---------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_principal = Ventana()
    ventana_principal.show()
    sys.exit(app.exec())
