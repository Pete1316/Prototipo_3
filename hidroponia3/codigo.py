import serial
import time

# 🔵 CAMBIA ESTE PUERTO
PUERTO = "COM13"     # COM Bluetooth
BAUD = 9600

try:
    print("Conectando por Bluetooth...")
    bt = serial.Serial(PUERTO, BAUD, timeout=1)
    time.sleep(2)

    print("✅ Conectado al ESP32 por Bluetooth")

    while True:
        print("\nComandos:")
        print("1 → Modo MANUAL")
        print("2 → Modo AUTOMÁTICO")
        print("q → Salir")

        op = input("Opción: ")

        if op == "1":
            tds = input("TDS: ")
            ph  = input("pH: ")
            ec  = input("EC: ")

            cmd = f"MANUAL,{tds},{ph},{ec}\n"
            bt.write(cmd.encode())
            print("📤 Enviado:", cmd.strip())

        elif op == "2":
            bt.write(b"AUTO\n")
            print("📤 Enviado: AUTO")

        elif op.lower() == "q":
            break

        # 🔁 Leer respuesta ESP32
        if bt.in_waiting:
            resp = bt.readline().decode(errors="ignore").strip()
            print("📥 ESP32:", resp)

except serial.SerialException as e:
    print("❌ Error de conexión:", e)

finally:
    try:
        bt.close()
        print("🔌 Conexión cerrada")
    except:
        pass
