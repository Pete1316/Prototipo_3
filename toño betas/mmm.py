import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, ttk
from dotenv import load_dotenv
import os
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
from fpdf import FPDF

# ========================
# Cargar variables de entorno
# ========================
load_dotenv()
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# ========================
# Función para enviar correo con PDF adjunto
# ========================
def enviar_correo_pdf(destinatario, asunto, mensaje, archivo_pdf):
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        print("❌ No se encontraron las credenciales de correo en .env")
        return

    msg = MIMEMultipart()
    msg["Subject"] = asunto
    msg["From"] = EMAIL_SENDER
    msg["To"] = destinatario
    msg.attach(MIMEText(mensaje))

    with open(archivo_pdf, "rb") as f:
        adjunto = MIMEApplication(f.read(), _subtype="pdf")
        adjunto.add_header('Content-Disposition', 'attachment', filename=os.path.basename(archivo_pdf))
        msg.attach(adjunto)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_SENDER, destinatario, msg.as_string())
        print(f"✅ Correo enviado a {destinatario}")
    except Exception as e:
        print(f"❌ Error al enviar correo: {e}")

# ========================
# Conexión a MySQL
# ========================
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="facturacion"
    )
    if conn.is_connected():
        print("✅ Conexión exitosa a MySQL")
        cursor = conn.cursor()
except Error as e:
    print("❌ Error de conexión:", e)
    exit()

# ========================
# Funciones de gestión de clientes
# ========================
def registrar_cliente():
    nombre = entry_nombre.get()
    identificacion = entry_identificacion.get()
    correo = entry_correo.get()
    direccion = entry_direccion.get()

    if not nombre or not identificacion:
        messagebox.showwarning("Campos requeridos", "El nombre y la identificación son obligatorios.")
        return

    try:
        cursor.execute(
            "INSERT INTO clientes (nombre, identificacion, correo, direccion) VALUES (%s, %s, %s, %s)",
            (nombre, identificacion, correo, direccion)
        )
        conn.commit()
        messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
        limpiar_campos()
        mostrar_clientes()
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "La identificación ya existe.")

def editar_cliente():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selección requerida", "Selecciona un cliente para editar.")
        return

    cliente_id = tree.item(selected[0])["values"][0]

    cursor.execute(
        "UPDATE clientes SET nombre=%s, identificacion=%s, correo=%s, direccion=%s WHERE id=%s",
        (entry_nombre.get(), entry_identificacion.get(), entry_correo.get(), entry_direccion.get(), cliente_id)
    )
    conn.commit()
    messagebox.showinfo("Éxito", "Cliente actualizado.")
    limpiar_campos()
    mostrar_clientes()

def eliminar_cliente():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selección requerida", "Selecciona un cliente para eliminar.")
        return

    cliente_id = tree.item(selected[0])["values"][0]

    cursor.execute("DELETE FROM clientes WHERE id=%s", (cliente_id,))
    conn.commit()
    messagebox.showinfo("Éxito", "Cliente eliminado.")
    mostrar_clientes()

def buscar_cliente():
    for row in tree.get_children():
        tree.delete(row)

    busqueda = entry_buscar.get()
    cursor.execute(
        "SELECT * FROM clientes WHERE identificacion LIKE %s OR nombre LIKE %s",
        (f"%{busqueda}%", f"%{busqueda}%")
    )
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

def mostrar_clientes():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM clientes")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_identificacion.delete(0, tk.END)
    entry_correo.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)
    for item in tree_productos.get_children():
        tree_productos.delete(item)

def seleccionar_cliente(event):
    selected = tree.selection()
    if selected:
        cliente = tree.item(selected[0])["values"]
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, cliente[1])
        entry_identificacion.delete(0, tk.END)
        entry_identificacion.insert(0, cliente[2])
        entry_correo.delete(0, tk.END)
        entry_correo.insert(0, cliente[3])
        entry_direccion.delete(0, tk.END)
        entry_direccion.insert(0, cliente[4])

# ========================
# Función para generar PDF y enviar
# ========================
def enviar_datos_cliente_pdf():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selección requerida", "Selecciona un cliente para enviar los datos.")
        return

    cliente = tree.item(selected[0])["values"]
    nombre, identificacion, correo, direccion = cliente[1], cliente[2], cliente[3], cliente[4]

    if not correo:
        messagebox.showwarning("Sin correo", "El cliente no tiene un correo registrado.")
        return

    # Obtener productos del Treeview
    productos = []
    for item in tree_productos.get_children():
        prod, cant, precio = tree_productos.item(item)["values"]
        productos.append({"producto": prod, "cantidad": cant, "precio": precio})

    if not productos:
        messagebox.showwarning("Sin productos", "Agrega al menos un producto.")
        return

    # Crear PDF con FPDF
    pdf = FPDF()
    pdf.add_page()

    # Agregar fuente personalizada (Borel Regular)
    pdf.add_font('Borel', '', r'D:\visualcode\toño\Borel\Borel-Regular.ttf')
    pdf.set_font('Borel', '', 16)

    pdf.cell(0, 10, "Factura Electrónica", ln=True, align="C")
    pdf.set_font('Borel', '', 12)
    pdf.ln(5)
    pdf.cell(0, 8, f"Cliente: {nombre}", ln=True)
    pdf.cell(0, 8, f"ID: {identificacion}", ln=True)
    pdf.cell(0, 8, f"Correo: {correo}", ln=True)
    pdf.ln(5)

    # Tabla de productos
    pdf.set_font('Borel', '', 12)
    pdf.cell(80, 8, "Producto", border=1)
    pdf.cell(30, 8, "Cantidad", border=1)
    pdf.cell(30, 8, "Precio", border=1)
    pdf.cell(30, 8, "Subtotal", border=1, ln=True)

    total = 0
    fill = False
    for p in productos:
        subtotal = p["cantidad"] * p["precio"]
        total += subtotal
        if fill:
            pdf.set_fill_color(230, 230, 230)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.cell(80, 8, p["producto"], border=1, fill=True)
        pdf.cell(30, 8, str(p["cantidad"]), border=1, fill=True)
        pdf.cell(30, 8, f"${p['precio']:.2f}", border=1, fill=True)
        pdf.cell(30, 8, f"${subtotal:.2f}", border=1, ln=True, fill=True)
        fill = not fill

    pdf.cell(140, 8, "Total", border=1)
    pdf.cell(30, 8, f"${total:.2f}", border=1, ln=True)

    archivo_pdf = f"{nombre}_factura.pdf"
    pdf.output(archivo_pdf)

    # Enviar correo con PDF adjunto
    asunto = f"Factura Electrónica - {nombre}"
    mensaje = f"Hola {nombre},\n\nAdjunto tu factura en PDF."
    enviar_correo_pdf(correo, asunto, mensaje, archivo_pdf)
    messagebox.showinfo("Correo enviado", f"Se enviaron los datos al correo: {correo}")

# ========================
# Interfaz gráfica (Tkinter)
# ========================
root = tk.Tk()
root.title("Gestión de Clientes - Facturación Electrónica")
root.geometry("900x700")

# --- Formulario Cliente ---
frame_form = tk.LabelFrame(root, text="Datos del Cliente", padx=10, pady=10)
frame_form.pack(fill="x", padx=10, pady=5)

tk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="w")
entry_nombre = tk.Entry(frame_form, width=30)
entry_nombre.grid(row=0, column=1)

tk.Label(frame_form, text="Identificación:").grid(row=1, column=0, sticky="w")
entry_identificacion = tk.Entry(frame_form, width=30)
entry_identificacion.grid(row=1, column=1)

tk.Label(frame_form, text="Correo:").grid(row=2, column=0, sticky="w")
entry_correo = tk.Entry(frame_form, width=30)
entry_correo.grid(row=2, column=1)

tk.Label(frame_form, text="Dirección:").grid(row=3, column=0, sticky="w")
entry_direccion = tk.Entry(frame_form, width=30)
entry_direccion.grid(row=3, column=1)

# --- Botones Cliente ---
frame_btn = tk.Frame(root)
frame_btn.pack(fill="x", padx=10, pady=5)

btn_registrar = tk.Button(frame_btn, text="Registrar", command=registrar_cliente, bg="green", fg="white")
btn_registrar.pack(side="left", padx=5)
btn_editar = tk.Button(frame_btn, text="Editar", command=editar_cliente, bg="blue", fg="white")
btn_editar.pack(side="left", padx=5)
btn_eliminar = tk.Button(frame_btn, text="Eliminar", command=eliminar_cliente, bg="red", fg="white")
btn_eliminar.pack(side="left", padx=5)
btn_limpiar = tk.Button(frame_btn, text="Limpiar", command=limpiar_campos)
btn_limpiar.pack(side="left", padx=5)
btn_enviar_pdf = tk.Button(frame_btn, text="Generar Factura PDF", command=enviar_datos_cliente_pdf, bg="orange", fg="white")
btn_enviar_pdf.pack(side="left", padx=5)

# --- Búsqueda ---
frame_buscar = tk.LabelFrame(root, text="Buscar Cliente")
frame_buscar.pack(fill="x", padx=10, pady=5)

entry_buscar = tk.Entry(frame_buscar, width=40)
entry_buscar.pack(side="left", padx=5)
btn_buscar = tk.Button(frame_buscar, text="Buscar", command=buscar_cliente)
btn_buscar.pack(side="left", padx=5)
btn_mostrar = tk.Button(frame_buscar, text="Mostrar Todos", command=mostrar_clientes)
btn_mostrar.pack(side="left", padx=5)

# --- Tabla Clientes ---
frame_tabla = tk.Frame(root)
frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("ID", "Nombre", "Identificación", "Correo", "Dirección")
tree = ttk.Treeview(frame_tabla, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=140)
tree.pack(fill="both", expand=True)
tree.bind("<<TreeviewSelect>>", seleccionar_cliente)

# --- Frame Productos ---
frame_productos = tk.LabelFrame(root, text="Productos", padx=10, pady=10)
frame_productos.pack(fill="x", padx=10, pady=5)

tk.Label(frame_productos, text="Producto:").grid(row=0, column=0)
entry_producto = tk.Entry(frame_productos, width=20)
entry_producto.grid(row=0, column=1)
tk.Label(frame_productos, text="Cantidad:").grid(row=0, column=2)
entry_cantidad = tk.Entry(frame_productos, width=10)
entry_cantidad.grid(row=0, column=3)
tk.Label(frame_productos, text="Precio:").grid(row=0, column=4)
entry_precio = tk.Entry(frame_productos, width=10)
entry_precio.grid(row=0, column=5)
btn_agregar_producto = tk.Button(frame_productos, text="Agregar Producto", command=lambda: agregar_producto())
btn_agregar_producto.grid(row=0, column=6, padx=5)

columns_prod = ("Producto", "Cantidad", "Precio")
tree_productos = ttk.Treeview(frame_productos, columns=columns_prod, show="headings", height=5)
for col in columns_prod:
    tree_productos.heading(col, text=col)
    tree_productos.column(col, width=100)
tree_productos.grid(row=1, column=0, columnspan=7, pady=5)

def agregar_producto():
    producto = entry_producto.get()
    try:
        cantidad = float(entry_cantidad.get())
        precio = float(entry_precio.get())
    except ValueError:
        messagebox.showerror("Error", "Cantidad y Precio deben ser números.")
        return
    if not producto:
        messagebox.showerror("Error", "El producto es obligatorio.")
        return
    tree_productos.insert("", tk.END, values=(producto, cantidad, precio))
    entry_producto.delete(0, tk.END)
    entry_cantidad.delete(0, tk.END)
    entry_precio.delete(0, tk.END)

# --- Mostrar datos iniciales ---
mostrar_clientes()
root.mainloop()
