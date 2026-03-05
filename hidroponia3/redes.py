import subprocess
from concurrent.futures import ThreadPoolExecutor

# ===== Configuración =====
RED_BASE = "192.168.0."
MAX_HILOS = 50   # cuantos pings en paralelo

fabricantes = {
    "F0:99:B6": "Apple",
    "3C:5A:B4": "Samsung",
    "44:07:0B": "Xiaomi",
    "D8:3A:DD": "Huawei"
}

# ===== Función ping =====
def ping(ip):
    subprocess.run(
        ["ping", "-n", "1", "-w", "80", ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

# ===== Paso 1: Ping paralelo =====
print("Escaneando red (modo rápido)...")

ips = [RED_BASE + str(i) for i in range(1, 255)]

with ThreadPoolExecutor(max_workers=MAX_HILOS) as executor:
    executor.map(ping, ips)

# ===== Paso 2: Leer ARP =====
arp = subprocess.run(["arp", "-a"], capture_output=True, text=True)

dispositivos = []

for linea in arp.stdout.splitlines():
    partes = linea.split()
    if len(partes) >= 3 and "-" in partes[1]:
        ip = partes[0]
        mac = partes[1].replace("-", ":").upper()
        tipo = partes[2]

        # filtros
        if ip.startswith(("224.", "239.")):
            continue
        if ip.endswith(".255") or ip == "255.255.255.255":
            continue
        if mac == "FF:FF:FF:FF:FF:FF":
            continue
        if tipo != "dinámico":
            continue

        dispositivos.append((ip, mac))

# ===== Fabricante =====
def obtener_fabricante(mac):
    return fabricantes.get(mac[:8], "Desconocido")

# ===== Resultado =====
print("\nDispositivos detectados:\n")
for ip, mac in dispositivos:
    print(f"IP: {ip} | MAC: {mac} | Marca: {obtener_fabricante(mac)}")
