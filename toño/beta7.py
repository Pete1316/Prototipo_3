import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, ttk
from dotenv import load_dotenv
import os, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
from fpdf import FPDF


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FUENTE_PATH = os.path.join(BASE_DIR, "Borel", "Borel-Regular.ttf")
OFL_PATH = os.path.join(BASE_DIR, "Borel", "OFL.txt")


load_dotenv()
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")



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


try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="facturacion"
    )
    if conn.is_connected():
        print("✅ Conexión exitosa a MySQL")
        cursor = conn.cursor(dictionary=True)
except Error as e:
    print("❌ Error de conexión:", e)
    exit()


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
            "INSERT INTO clientes (nombre, identificacion, correo, direccion) VALUES (%s,%s,%s,%s)",
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
        tree.insert("", tk.END, values=(row["id"], row["nombre"], row["identificacion"], row["correo"], row["direccion"]))

def mostrar_clientes():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM clientes")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=(row["id"], row["nombre"], row["identificacion"], row["correo"], row["direccion"]))

def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_identificacion.delete(0, tk.END)
    entry_correo.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)
    for item in tree_productos.get_children():
        tree_productos.delete(item)
    label_total_var.set("0.00")

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
# Productos
# ========================
def cargar_productos_db():
    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()
    combo_producto['values'] = [f"{p['nombre']} (${p['precio']})" for p in productos]

def agregar_producto():
    sel = combo_producto.get()
    if not sel:
        messagebox.showerror("Error", "Selecciona un producto")
        return
    nombre = sel.split(" ($")[0]
    precio = float(sel.split(" ($")[1][:-1])
    try:
        cantidad = float(entry_cantidad.get())
    except ValueError:
        messagebox.showerror("Error", "Cantidad debe ser un número")
        return
    subtotal = cantidad * precio
    tree_productos.insert("", tk.END, values=(nombre, f"{cantidad:.2f}", f"{precio:.2f}", f"{subtotal:.2f}"))
    entry_cantidad.delete(0, tk.END)
    actualizar_total()

def eliminar_producto():
    selected = tree_productos.selection()
    if not selected:
        messagebox.showwarning("Selección requerida", "Selecciona un producto para eliminar")
        return
    for sel in selected:
        tree_productos.delete(sel)
    actualizar_total()

def actualizar_total():
    total = 0
    for i in tree_productos.get_children():
        total += float(tree_productos.item(i)["values"][3])
    label_total_var.set(f"{total:.2f}")

# ========================
# Factura
# ========================
def generar_factura_pdf():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selección requerida", "Selecciona un cliente")
        return
    cliente = tree.item(selected[0])["values"]
    cliente_id, nombre, identificacion, correo, direccion = cliente
    if not tree_productos.get_children():
        messagebox.showwarning("Sin productos", "Agrega al menos un producto antes de generar la factura.")
        return
    total = sum([float(tree_productos.item(i)["values"][3]) for i in tree_productos.get_children()])

    # PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('Borel', '', FUENTE_PATH, uni=True)
    pdf.set_font('Borel', '', 16)
    pdf.cell(0, 10, "Factura Electrónica", ln=True, align="C")
    pdf.set_font('Borel', '', 12)
    pdf.cell(0, 8, f"Cliente: {nombre}", ln=True)
    pdf.cell(0, 8, f"ID: {identificacion}", ln=True)
    pdf.cell(0, 8, f"Correo: {correo}", ln=True)
    pdf.cell(0, 8, f"Dirección: {direccion}", ln=True)
    pdf.ln(5)

    pdf.cell(80, 8, "Producto", border=1)
    pdf.cell(30, 8, "Cantidad", border=1)
    pdf.cell(30, 8, "Precio", border=1)
    pdf.cell(30, 8, "Subtotal", border=1, ln=True)

    for i in tree_productos.get_children():
        p, cant, precio, subtotal = tree_productos.item(i)["values"]
        pdf.cell(80,8,str(p),border=1)
        pdf.cell(30,8,str(cant),border=1)
        pdf.cell(30,8,f"${precio}",border=1)
        pdf.cell(30,8,f"${subtotal}",border=1,ln=True)

    pdf.cell(140,8,"Total",border=1)
    pdf.cell(30,8,f"${total:.2f}",border=1,ln=True)
    archivo_pdf = os.path.join(BASE_DIR, f"{nombre}_factura.pdf")
    pdf.output(archivo_pdf)

    # Guardar factura en DB
    cursor.execute("INSERT INTO facturas (cliente_id, total, archivo_pdf) VALUES (%s,%s,%s)",
                   (cliente_id, total, archivo_pdf))
    conn.commit()

    # Enviar correo
    if correo:
        asunto = f"Factura Electrónica - {nombre}"
        mensaje = f"Hola {nombre},\n\nAdjunto tu factura en PDF."
        enviar_correo_pdf(correo, asunto, mensaje, archivo_pdf)
        messagebox.showinfo("Factura", f"Factura enviada a {correo}")
    else:
        messagebox.showinfo("Factura", "Factura generada y guardada en la base de datos.")

# ========================
# Interfaz
# ========================
root = tk.Tk()
root.title("Gestión de Clientes - Facturación Electrónica")
root.geometry("1200x700")

# Variables
label_total_var = tk.StringVar(value="0.00")

# Frames productos y clientes
frame_prod = tk.LabelFrame(root, text="Productos", padx=10, pady=10)
frame_form = tk.LabelFrame(root, text="Datos del Cliente", padx=10, pady=10)
frame_prod.grid(row=0, column=0, sticky="n", padx=10, pady=5)
frame_form.grid(row=0, column=1, sticky="n", padx=10, pady=5)

# Contenido frame productos
tk.Label(frame_prod, text="Producto:").grid(row=0, column=0, sticky="w")
combo_producto = ttk.Combobox(frame_prod, width=30)
combo_producto.grid(row=0, column=1)
tk.Label(frame_prod, text="Cantidad:").grid(row=0, column=2, sticky="w")
entry_cantidad = tk.Entry(frame_prod, width=10)
entry_cantidad.grid(row=0, column=3)
btn_agregar = tk.Button(frame_prod, text="Agregar Producto", command=agregar_producto)
btn_agregar.grid(row=0, column=4, padx=5)
btn_eliminar_prod = tk.Button(frame_prod, text="Eliminar Producto", command=eliminar_producto, bg="red", fg="white")
btn_eliminar_prod.grid(row=0, column=5, padx=5)

columns_prod = ("Producto","Cantidad","Precio","Subtotal")
tree_productos = ttk.Treeview(frame_prod, columns=columns_prod, show="headings", height=10)
for col in columns_prod:
    tree_productos.heading(col, text=col)
    tree_productos.column(col, width=100)
tree_productos.grid(row=1,column=0,columnspan=6,pady=5)

tk.Label(frame_prod, text="Total: $").grid(row=2,column=2,sticky="e")
tk.Label(frame_prod, textvariable=label_total_var).grid(row=2,column=3,sticky="w")

# Contenido frame clientes
tk.Label(frame_form, text="Nombre:").grid(row=0,column=0,sticky="w")
entry_nombre = tk.Entry(frame_form, width=30)
entry_nombre.grid(row=0,column=1)
tk.Label(frame_form, text="Identificación:").grid(row=1,column=0,sticky="w")
entry_identificacion = tk.Entry(frame_form, width=30)
entry_identificacion.grid(row=1,column=1)
tk.Label(frame_form, text="Correo:").grid(row=2,column=0,sticky="w")
entry_correo = tk.Entry(frame_form, width=30)
entry_correo.grid(row=2,column=1)
tk.Label(frame_form, text="Dirección:").grid(row=3,column=0,sticky="w")
entry_direccion = tk.Entry(frame_form, width=30)
entry_direccion.grid(row=3,column=1)

# Botones
frame_btn = tk.Frame(frame_form)
frame_btn.grid(row=4,column=0,columnspan=2,pady=10)
btn_registrar = tk.Button(frame_btn,text="Registrar",command=registrar_cliente,bg="green",fg="white")
btn_registrar.pack(side="left", padx=5)
btn_editar = tk.Button(frame_btn,text="Editar",command=editar_cliente,bg="blue",fg="white")
btn_editar.pack(side="left", padx=5)
btn_eliminar = tk.Button(frame_btn,text="Eliminar",command=eliminar_cliente,bg="red",fg="white")
btn_eliminar.pack(side="left", padx=5)
btn_limpiar = tk.Button(frame_btn,text="Limpiar",command=limpiar_campos)
btn_limpiar.pack(side="left", padx=5)
btn_pdf = tk.Button(frame_btn,text="Generar Factura PDF",command=generar_factura_pdf,bg="orange",fg="white")
btn_pdf.pack(side="left", padx=5)

# Búsqueda
frame_buscar = tk.LabelFrame(root,text="Buscar Cliente")
frame_buscar.grid(row=1,column=0,columnspan=2,sticky="we",padx=10,pady=5)
entry_buscar = tk.Entry(frame_buscar,width=40)
entry_buscar.pack(side="left", padx=5)
btn_buscar = tk.Button(frame_buscar,text="Buscar",command=buscar_cliente)
btn_buscar.pack(side="left", padx=5)
btn_mostrar = tk.Button(frame_buscar,text="Mostrar Todos",command=mostrar_clientes)
btn_mostrar.pack(side="left", padx=5)

# Tabla clientes
frame_tabla = tk.Frame(root)
frame_tabla.grid(row=2,column=0,columnspan=2,sticky="nsew",padx=10,pady=10)
columns = ("ID","Nombre","Identificación","Correo","Dirección")
tree = ttk.Treeview(frame_tabla, columns=columns, show="headings")
for col in columns:
    tree.heading(col,text=col)
    tree.column(col,width=140)
tree.pack(fill="both",expand=True)
tree.bind("<<TreeviewSelect>>", seleccionar_cliente)

# Inicializar
cargar_productos_db()
mostrar_clientes()
root.mainloop()
