from fpdf import FPDF

# Datos de ejemplo
cliente = {"nombre": "Juan Pérez", "id": "123456789", "correo": "juan@example.com"}
productos = [
    {"producto": "Tomate", "cantidad": 3, "precio": 2.5},
    {"producto": "Lechuga", "cantidad": 2, "precio": 1.8},
    {"producto": "Cebolla", "cantidad": 5, "precio": 1.2}
]

pdf = FPDF()
pdf.add_page()

# Agregar fuente personalizada (solo Regular)
pdf.add_font('Borel', '', r'D:\visualcode\toño\Borel\Borel-Regular.ttf')
pdf.set_font('Borel', '', 16)

# Encabezado
pdf.cell(0, 10, "Factura Electrónica", ln=True, align="C")

# Datos del cliente
pdf.set_font('Borel', '', 12)
pdf.ln(5)
pdf.cell(0, 8, f"Cliente: {cliente['nombre']}", ln=True)
pdf.cell(0, 8, f"ID: {cliente['id']}", ln=True)
pdf.cell(0, 8, f"Correo: {cliente['correo']}", ln=True)

# Tabla de productos
pdf.ln(10)
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

# Total
pdf.cell(140, 8, "Total", border=1)
pdf.cell(30, 8, f"${total:.2f}", border=1, ln=True)

# Guardar PDF
pdf.output("factura.pdf")
