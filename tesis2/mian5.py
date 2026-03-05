import sys
import re
import time
from collections import deque

from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame, QLineEdit, QMessageBox, QComboBox
)
import serial
import serial.tools.list_ports

# --------------------
# Serial Reader Thread
# --------------------
class SerialReader(QThread):
    received = Signal(str)
    status = Signal(str)

    def __init__(self, port: str, baud: int = 9600, parent=None):
        super().__init__(parent)
        self.port = port
        self.baud = baud
        self._running = True
        self._ser = None

    def run(self):
        while self._running:
            if self._ser is None:
                try:
                    self._ser = serial.Serial(self.port, self.baud, timeout=1)
                    self.status.emit(f"Conectado a {self.port} @ {self.baud}")
                except Exception as e:
                    self.status.emit(f"No conectado: {e}")
                    self._ser = None
                    self.msleep(1500)
                    continue

            try:
                line = self._ser.readline().decode(errors="ignore").strip()
                if line:
                    self.received.emit(line)
            except Exception as e:
                self.status.emit(f"Error lectura: {e}")
                try:
                    self._ser.close()
                except:
                    pass
                self._ser = None
                self.msleep(1000)

    def stop(self):
        self._running = False
        if self._ser:
            try:
                self._ser.close()
            except:
                pass
        self.wait(2000)

    def change_port(self, new_port):
        if self._ser:
            try:
                self._ser.close()
            except:
                pass
            self._ser = None
        self.port = new_port


# --------------------
# Dashboard
# --------------------
class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hidroponia - Dashboard")
        self.setMinimumSize(760, 420)
        self._serial_thread = None

        self.ph = None
        self.temp = None
        self.hum = None
        self.nivel = None

        self._init_ui()
        self._start_status_timer()

    # -----------------
    # UI
    # -----------------
    def _init_ui(self):
        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)

        self.port_combo = QComboBox()
        self.refresh_ports()
        self.port_combo.setEditable(False)

        self.refresh_btn = QPushButton("Refrescar puertos")
        self.connect_btn = QPushButton("Conectar")
        self.disconnect_btn = QPushButton("Desconectar")
        self.disconnect_btn.setEnabled(False)

        self.status_label = QLabel("Estado: No conectado")
        self.status_label.setMinimumWidth(300)

        top_layout.addWidget(QLabel("Puerto:"))
        top_layout.addWidget(self.port_combo)
        top_layout.addWidget(self.refresh_btn)
        top_layout.addWidget(self.connect_btn)
        top_layout.addWidget(self.disconnect_btn)
        top_layout.addStretch(1)
        top_layout.addWidget(self.status_label)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)

        self.ph_card = self._make_card("pH", " — ", large=True)

        self.temp_card = self._make_card("Temperatura", "— °C")
        self.hum_card = self._make_card("Humedad", "— %")
        temp_hum_layout = QVBoxLayout()
        temp_hum_layout.addWidget(self.temp_card)
        temp_hum_layout.addWidget(self.hum_card)

        self.nivel_card = self._make_card("Nivel de Agua", "—", small=True)

        main_layout.addWidget(self.ph_card, 3)
        main_layout.addLayout(temp_hum_layout, 2)
        main_layout.addWidget(self.nivel_card, 1)

        bottom_layout = QHBoxLayout()
        self.last_msg_label = QLabel("Último mensaje: —")
        bottom_layout.addWidget(self.last_msg_label)

        layout = QVBoxLayout(self)
        layout.addLayout(top_layout)
        layout.addLayout(main_layout)
        layout.addLayout(bottom_layout)

        self.refresh_btn.clicked.connect(self.refresh_ports)
        self.connect_btn.clicked.connect(self.start_serial)
        self.disconnect_btn.clicked.connect(self.stop_serial)

        self._parse_queue = deque(maxlen=50)

    # -----------------
    # SOLO LO QUE PEDISTE: COMUNICACIÓN ARREGLADA
    # -----------------
    def refresh_ports(self):
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()

        encontrados = 0
        for p in ports:
            desc = p.description.lower()
            dev = p.device

            # Filtrar SOLO el HC-05 / Bluetooth SPP OUT
            if ("spp" in desc) or ("bluetooth" in desc) or ("hc" in desc):
                self.port_combo.addItem(f"{dev} — {p.description}", dev)
                encontrados += 1

        # Seleccionar automáticamente COM7 si está
        for i in range(self.port_combo.count()):
            if "COM7" in self.port_combo.itemText(i):
                self.port_combo.setCurrentIndex(i)
                break

        if encontrados == 0:
            self.port_combo.addItem("No hay puertos Bluetooth", "")

    def start_serial(self):
        port = self.port_combo.currentData()
        if not port:
            QMessageBox.warning(self, "Puerto", "Selecciona un puerto válido.")
            return

        print("Intentando conectar a:", port)

        if self._serial_thread and self._serial_thread.isRunning():
            self._serial_thread.change_port(port)
            self.status_label.setText(f"Cambiando puerto a {port}...")
            return

        self._serial_thread = SerialReader(port, 9600)
        self._serial_thread.received.connect(self.on_serial_line)
        self._serial_thread.status.connect(self.on_status)
        self._serial_thread.start()
        self.connect_btn.setEnabled(False)
        self.disconnect_btn.setEnabled(True)

    def stop_serial(self):
        if self._serial_thread:
            self._serial_thread.stop()
            self._serial_thread = None
        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)
        self.status_label.setText("Estado: Desconectado")

    # -----------------
    # Status & Parsing
    # -----------------
    def on_status(self, text):
        self.status_label.setText(f"Estado: {text}")

    def on_serial_line(self, line: str):
        self.last_msg_label.setText(f"Último mensaje: {line}")
        parsed = self.parse_sensor_line(line)
        if parsed:
            self.update_values(parsed)

    def parse_sensor_line(self, line: str):
        d = {}
        try:
            parts = re.split(r"\s*\|\s*|\s*,\s*|\s*;\s*", line)
            for p in parts:
                if ':' in p:
                    key, val = p.split(':', 1)
                    key = key.strip().lower()
                    val = val.strip()
                    if key.startswith('ph'):
                        try:
                            d['ph'] = float(re.findall(r"[-+]?\d*\.\d+|\d+", val)[0])
                        except:
                            d['ph'] = None
                    elif key.startswith('temp') or key.startswith('t'):
                        try:
                            d['temp'] = float(re.findall(r"[-+]?\d*\.\d+|\d+", val)[0])
                        except:
                            d['temp'] = None
                    elif key.startswith('hum'):
                        try:
                            d['hum'] = float(re.findall(r"[-+]?\d*\.\d+|\d+", val)[0])
                        except:
                            d['hum'] = None
                    elif key.startswith('nivel'):
                        d['nivel'] = val.upper()
            return d
        except:
            return None

    def update_values(self, parsed: dict):
        if 'ph' in parsed:
            self.ph = parsed['ph']
            val = f"{self.ph:.2f}" if self.ph is not None else "—"
            self._set_card_value(self.ph_card, val)

            val_label = self.ph_card.findChild(QLabel, "value")
            if self.ph is None:
                val_label.setStyleSheet("font-size:40px; font-weight:700; color:#6b7280;")
            else:
                if 5.5 <= self.ph <= 8.0:
                    color = "#059669"
                elif 5.0 <= self.ph < 5.5 or 8.0 < self.ph <= 8.5:
                    color = "#d97706"
                else:
                    color = "#dc2626"
                val_label.setStyleSheet(f"font-size:40px; font-weight:700; color:{color};")

        if 'temp' in parsed:
            self.temp = parsed['temp']
            self._set_card_value(self.temp_card, f"{self.temp:.1f} °C" if self.temp is not None else "—")

        if 'hum' in parsed:
            self.hum = parsed['hum']
            self._set_card_value(self.hum_card, f"{self.hum:.1f} %" if self.hum is not None else "—")

        if 'nivel' in parsed:
            self.nivel = parsed['nivel']
            if "BAJO" in self.nivel or "LOW" in self.nivel:
                self._set_card_value(self.nivel_card, "BAJO")
                val_label = self.nivel_card.findChild(QLabel, "value")
                val_label.setStyleSheet("font-size:20px; font-weight:700; color:#dc2626;")
            else:
                self._set_card_value(self.nivel_card, "OK")
                val_label = self.nivel_card.findChild(QLabel, "value")
                val_label.setStyleSheet("font-size:20px; font-weight:700; color:#059669;")

    def _set_card_value(self, card: QFrame, text: str):
        val_label = card.findChild(QLabel, "value")
        if val_label:
            val_label.setText(text)

    def _start_status_timer(self):
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.refresh_ports)
        self._timer.start(10000)

    def closeEvent(self, event):
        if self._serial_thread:
            self._serial_thread.stop()
        event.accept()


# --------------------
# Main
# --------------------
def main():
    app = QApplication(sys.argv)
    dash = Dashboard()
    dash.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
