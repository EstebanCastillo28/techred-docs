from flask import Flask, render_template, request, send_file, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle
from io import BytesIO
import textwrap

app = Flask(__name__, template_folder="../templates", static_folder="../static")

# ──────────────────────────────────────────
#  HELPERS
# ──────────────────────────────────────────
def txt(c, x, y, val, size=9, bold=False):
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    c.setFillColor(colors.black)
    c.drawString(x, y, str(val or ""))

def label_field(c, lbl, val, x, y, lbl_w=22*mm, field_w=60*mm, size=9):
    txt(c, x, y, lbl, size, True)
    txt(c, x + lbl_w, y, val, size)
    c.setLineWidth(0.4)
    c.line(x + lbl_w - 1, y - 2.5, x + lbl_w + field_w, y - 2.5)

def wrap(c, text, x, y, max_w, font="Helvetica", size=9, leading=12, max_lines=4):
    c.setFont(font, size)
    from reportlab.pdfbase.pdfmetrics import stringWidth
    words = str(text or "").split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if stringWidth(t, font, size) <= max_w:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
            if len(lines) >= max_lines: break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    for i, ln in enumerate(lines):
        c.drawString(x, y - i * leading, ln)

def draw_logo(c, x, y):
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(colors.black)
    c.drawString(x, y, "TECH")
    c.setFillColor(colors.HexColor("#e83030"))
    c.drawString(x + 31*mm, y, "RED")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 8)
    c.drawString(x, y - 7*mm, "Tecnología e Infraestructura")
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x, y - 12.5*mm, "NIT. 900.866.525-6")
    c.drawString(x, y - 17*mm, "CLL 68 # 23-61 7 DE AGOSTO")
    c.drawString(x, y - 21.5*mm, "CORREO: VANTILISTO@TECHRED.COM.CO")
    c.drawString(x, y - 26*mm, "www.techred.com.co")

def footer_bar(c, width):
    c.setFillColor(colors.HexColor("#e83030"))
    c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(width/2, 22*mm,
        "Línea de servicio al cliente y garantías  –  WhatsApp: 302 5555083  –  servicio.cliente@techred.com.co")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(width/2, 16*mm,
        "Conozca más en www.techred.com.co/pages/politicas-de-privacidad")
    c.drawCentredString(width/2, 11*mm,
        "Aplican T&C. Este producto es comercializado y distribuido por Techred S.A.S. Vanti Listo actúa únicamente como medio de financiamiento. © Techred S.A.S 2026")

# ──────────────────────────────────────────
#  PDF 1 – ORDEN DE PEDIDO
# ──────────────────────────────────────────
def pdf_orden(d):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    W, H = A4
    m = 16*mm

    draw_logo(c, m, H - 22*mm)

    # Cliente block
    rx = 82*mm
    ty = H - 22*mm
    label_field(c, "CLIENTE:",    d.get("cliente"),   rx, ty,           22*mm, 78*mm)
    label_field(c, "C.C:",        d.get("cc"),         rx, ty-9*mm,      12*mm, 28*mm)
    label_field(c, "TEL/CEL:",    d.get("tel"),        rx+45*mm, ty-9*mm, 16*mm, 30*mm)
    label_field(c, "DIRECCIÓN:",  d.get("direccion"),  rx, ty-18*mm,     20*mm, 70*mm)
    label_field(c, "BARRIO:",     d.get("barrio"),     rx, ty-27*mm,     15*mm, 42*mm)
    label_field(c, "CIUDAD:",     d.get("ciudad"),     rx+62*mm, ty-27*mm,14*mm, 28*mm)
    label_field(c, "CONTACTO 1:", d.get("contacto1"), rx, ty-36*mm,     24*mm, 66*mm)
    label_field(c, "CONTACTO 2:", d.get("contacto2"), rx, ty-45*mm,     24*mm, 66*mm)
    label_field(c, "CORREO:",     d.get("correo"),    rx, ty-54*mm,     16*mm, 74*mm)

    # Caja derecha – Orden / Fecha / Cuenta
    bx = 166*mm
    c.setLineWidth(0.6)
    c.roundRect(bx, H-32*mm, 28*mm, 9*mm, 2)
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor("#e83030"))
    c.drawCentredString(bx+14*mm, H-26.8*mm, "ORDEN DE PEDIDO")
    c.setFillColor(colors.black)
    c.drawString(bx, H-40*mm, "FECHA DE PEDIDO")
    date_lbl = ["DIA","MES","AÑO"]
    date_val = [d.get("dia",""), d.get("mes",""), d.get("anio","")]
    for i,(lbl,val) in enumerate(zip(date_lbl,date_val)):
        bxx = bx + i*9.5*mm
        bww = 9*mm if i < 2 else 10*mm
        c.roundRect(bxx, H-49*mm, bww, 8*mm, 1)
        c.setFont("Helvetica-Bold", 5.5)
        c.drawCentredString(bxx+bww/2, H-43.5*mm, lbl)
        c.setFont("Helvetica", 8)
        c.drawCentredString(bxx+bww/2, H-47.2*mm, str(val))
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(bx, H-57*mm, "CUENTA CONTRATO")
    c.roundRect(bx, H-67*mm, 28*mm, 9*mm, 2)
    c.setFont("Helvetica", 9)
    c.drawCentredString(bx+14*mm, H-62.2*mm, str(d.get("cuenta_contrato","")))

    # Tabla ítems
    items = d.get("items", [])
    while len(items) < 4: items.append({})
    rows = [["REF","CANT","DESCRIPCION","VALOR PRODUCTO","CUOTAS","VALOR CUOTAS"]]
    for it in items[:4]:
        rows.append([it.get("ref",""), it.get("cant",""), it.get("descripcion",""),
                     it.get("valor_producto",""), it.get("cuotas",""), it.get("valor_cuotas","")])
    rows.append(["","","VALOR TOTAL DE LA COMPRA", f"$ {d.get('valor_total','')}","",""])

    tbl = Table(rows, colWidths=[22*mm,13*mm,80*mm,28*mm,17*mm,30*mm],
                rowHeights=[9*mm]+[10*mm]*4+[9*mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.black),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),8),
        ("GRID",(0,0),(-1,-1),0.5,colors.black),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("SPAN",(2,5),(5,5)),
        ("BACKGROUND",(0,5),(5,5),colors.black),
        ("TEXTCOLOR",(0,5),(5,5),colors.white),
        ("FONTNAME",(2,5),(5,5),"Helvetica-Bold"),
    ]))
    tbl_y = H - 130*mm
    tbl.wrapOn(c, W, H)
    tbl.drawOn(c, m, tbl_y)

    # Forma de pago
    py = tbl_y - 18*mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(m, py, "FORMA DE PAGO")
    pays = [("EFECTIVO:","efectivo"),("VANTI LISTO:","vanti_listo"),("OTRO","otro")]
    px = m
    for lbl,key in pays:
        c.setFont("Helvetica-Bold",9)
        c.drawString(px, py-9*mm, lbl)
        c.rect(px+24*mm, py-12*mm, 6*mm, 6*mm)
        if d.get(key):
            c.setFont("Helvetica-Bold",10)
            c.drawCentredString(px+27*mm, py-7.5*mm, "X")
        px += 42*mm

    label_field(c, "CONTRAENTREGA: $", d.get("contraentrega"), m, py-22*mm, 36*mm, 40*mm)
    label_field(c, "ASESOR:",          d.get("asesor"),         m, py-31*mm, 17*mm, 55*mm)
    label_field(c, "COD ASESOR:",      d.get("cod_asesor"),    m, py-40*mm, 24*mm, 48*mm)
    label_field(c, "SUPERVISOR:",      d.get("supervisor"),    m, py-49*mm, 24*mm, 48*mm)

    # Huella y firma
    hx, hy = 133*mm, py-54*mm
    c.roundRect(hx, hy, 23*mm, 32*mm, 3)
    c.setFont("Helvetica-Bold",8)
    c.drawCentredString(hx+11.5*mm, hy-6*mm, "HUELLA CLIENTE")
    c.line(168*mm, hy, 200*mm, hy)
    c.drawCentredString(184*mm, hy-6*mm, "FIRMA CLIENTE")

    footer_bar(c, W)
    c.showPage(); c.save(); buf.seek(0)
    return buf

# ──────────────────────────────────────────
#  PDF 2 – ACTA DE ENTREGA
# ──────────────────────────────────────────
def pdf_acta(d):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    W, H = A4
    m = 18*mm

    # Título
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(W/2, H-20*mm, "ACTA DE ENTREGA DE PRODUCTOS Y/O SERVICIOS TECHRED S.A.S")
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(W/2, H-27*mm, "FINANCIADOS A TRAVÉS DE LA FACTURA DEL SERVICIO DE GAS NATURAL DOMICILIARIO")
    c.setFont("Helvetica", 8)
    c.drawCentredString(W/2, H-32.5*mm, "ACTUALIZADA 10/02/2026")

    # Fecha + consecutivo
    fx = m
    fy = H-42*mm
    c.setFont("Helvetica-Bold",9)
    c.drawString(fx, fy, "FECHA DE GENERACIÓN:")
    for i,(lbl,val) in enumerate(zip(["D","M","A"],[d.get("dia",""),d.get("mes",""),d.get("anio","")])):
        bx2 = fx+47*mm+i*10*mm; bw2 = 9*mm
        c.roundRect(bx2, fy-7*mm, bw2, 7*mm, 1)
        c.setFont("Helvetica-Bold",5.5)
        c.drawCentredString(bx2+4.5*mm, fy-2.5*mm, lbl)
        c.setFont("Helvetica",8)
        c.drawCentredString(bx2+4.5*mm, fy-5.8*mm, str(val))
    c.setFont("Helvetica-Bold",9)
    c.drawString(fx+85*mm, fy, "CONSECUTIVO DE TALONARIO:")
    c.roundRect(fx+139*mm, fy-7*mm, 36*mm, 7*mm, 1)
    c.setFont("Helvetica",9)
    c.drawCentredString(fx+157*mm, fy-4*mm, str(d.get("consecutivo","")))

    # Título centrado
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(W/2, H-57*mm, "ACTA DE ENTREGA")

    # Párrafo intro
    para = (
        f"Con la firma del presente documento yo {d.get('cliente','')}, mayor de edad, identificado con tipo de documento "
        f"{d.get('tipo_documento','CC')} número {d.get('cc','')} y número de cuenta de pago (Recibo público Vanti) No. "
        f"{d.get('cuenta_contrato','')}, confirmo que he recibido a satisfacción el producto y/o servicio adquirido, "
        f"entregado en la dirección {d.get('direccion','')} de acuerdo a mi solicitud."
    )
    lines_para = textwrap.wrap(para, 115)
    c.setFont("Helvetica", 9)
    for i, ln in enumerate(lines_para[:5]):
        c.drawString(m, H-68*mm - i*5*mm, ln)

    # Tabla productos
    items = d.get("items",[])
    while len(items) < 7: items.append({})
    rows = [["DESCRIPCIÓN","CANTIDAD","VALOR"]] + \
           [[it.get("descripcion",""),it.get("cantidad",""),it.get("valor","")] for it in items[:7]]
    tbl = Table(rows, colWidths=[108*mm, 26*mm, 36*mm], rowHeights=[9*mm]+[9*mm]*7)
    tbl.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.5,colors.black),
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#e8e8e8")),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),9),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("ALIGN",(1,1),(-1,-1),"CENTER"),
    ]))
    tbl.wrapOn(c, W, H)
    tbl.drawOn(c, m, H-160*mm)

    # Políticas
    pol = (
        "POLÍTICAS DE DEVOLUCIÓN Y GARANTÍAS TECH RED S.A. El plazo máximo para solicitar cambio de productos son cinco (5) días "
        "calendario contados a partir de la fecha de entrega. Todos los artículos comercializados nuevos por TECH RED S.A.S. "
        "cuentan con una garantía de un (1) año. Para servicio al cliente: WhatsApp 3025555083 / vantilisto@techred.com.co"
    )
    for i, ln in enumerate(textwrap.wrap(pol, 150)[:6]):
        c.setFont("Helvetica", 7); c.drawString(m, H-174*mm - i*4*mm, ln)

    accept = (
        "Con la firma del presente documento manifiesto que entiendo y acepto el valor del producto, "
        "el valor de las cuotas pactadas, número de cuotas y todo lo contenido en este documento."
    )
    for i, ln in enumerate(textwrap.wrap(accept, 150)[:3]):
        c.setFont("Helvetica", 8); c.drawString(m, H-202*mm - i*5*mm, ln)

    c.setFont("Helvetica",9)
    c.drawString(m, H-222*mm, f"Para constancia se firma en la ciudad de {d.get('ciudad','')}, a los ___ días del mes de _______ del año ______")

    # Firmas
    sy = H-248*mm
    c.setFont("Helvetica-Bold",9)
    c.drawString(m+8*mm, sy+12*mm, "Datos de la persona que recibe")
    c.drawString(m+106*mm, sy+12*mm, "Datos de la persona que realiza la entrega")
    c.line(m, sy, m+75*mm, sy)
    c.line(m+98*mm, sy, m+173*mm, sy)
    c.drawString(m, sy+2*mm, "Firma:")
    c.drawString(m+98*mm, sy+2*mm, "Firma:")
    c.setFont("Helvetica",9)
    c.drawString(m, sy-8*mm, f"Nombre: {d.get('cliente','')}")
    c.drawString(m+98*mm, sy-8*mm, f"Nombre: {d.get('entrega_nombre','')}")
    c.drawString(m, sy-16*mm, f"CC: {d.get('cc','')}")
    c.drawString(m+98*mm, sy-16*mm, f"CC: {d.get('entrega_cc','')}")

    c.setFont("Helvetica",6.5)
    c.drawString(m, 9*mm,
        "NOTA LEGAL: El diligenciamiento incompleto o indebido de este formato ocasionará demoras en el proceso e incluso la cancelación del mismo.")

    c.showPage(); c.save(); buf.seek(0)
    return buf

# ──────────────────────────────────────────
#  PDF 3 – CAMBIO DE PRODUCTO
# ──────────────────────────────────────────
def pdf_cambio(d):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    W, H = A4
    m = 25*mm

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(W/2, H-28*mm, "Formato de Cambio de Producto")

    c.setFont("Helvetica-Bold",11)
    c.drawString(m, H-48*mm, "Bogotá")
    for i,(lbl,val,fw) in enumerate(zip(
        ["Día:","Mes:","Año:"],
        [d.get("dia",""),d.get("mes",""),d.get("anio","")],
        [14*mm, 14*mm, 18*mm]
    )):
        ox = m+30*mm+i*28*mm
        c.setFont("Helvetica-Bold",11); c.drawString(ox, H-48*mm, lbl)
        wl = 10*mm
        c.setFont("Helvetica",11); c.drawString(ox+wl+1, H-48*mm, str(val))
        c.line(ox+wl, H-50*mm, ox+wl+fw, H-50*mm)

    label_field(c, "Nombre del cliente:", d.get("cliente"),        m, H-65*mm, 44*mm, 100*mm, 11)
    label_field(c, "Cuenta contrato:",    d.get("cuenta_contrato"),m, H-80*mm, 36*mm, 70*mm,  11)

    c.setFont("Helvetica-Bold",11)
    c.drawString(m, H-100*mm, "Producto financiado (actual):")
    c.line(m, H-104*mm, W-m, H-104*mm)
    wrap(c, d.get("producto_actual"), m+2, H-112*mm, W-2*m-4, "Helvetica", 11, 7*mm, 3)

    c.setFont("Helvetica-Bold",11)
    c.drawString(m, H-132*mm, "Producto a cambiar:")
    c.line(m, H-136*mm, W-m, H-136*mm)
    wrap(c, d.get("producto_nuevo"), m+2, H-144*mm, W-2*m-4, "Helvetica", 11, 7*mm, 3)

    c.setFont("Helvetica-Bold",11)
    c.drawString(m, H-166*mm, "Motivo del cambio:")
    c.rect(m, H-215*mm, W-2*m, 45*mm)
    motivo_lines = textwrap.wrap(str(d.get("motivo","")), 88)
    c.setFont("Helvetica",10)
    for i, ln in enumerate(motivo_lines[:6]):
        c.drawString(m+4, H-180*mm - i*6*mm, ln)

    sy = H-248*mm
    c.setFont("Helvetica-Bold",10)
    c.drawString(m+8*mm, sy+14*mm, "Datos de la persona que recibe")
    c.drawString(m+103*mm, sy+14*mm, "Datos de la persona que realiza la entrega")
    c.line(m, sy, m+72*mm, sy)
    c.line(m+97*mm, sy, m+170*mm, sy)
    c.drawString(m, sy+2*mm, "Firma:")
    c.drawString(m+97*mm, sy+2*mm, "Firma:")
    c.setFont("Helvetica",9)
    c.drawString(m, sy-9*mm,  f"Nombre: {d.get('cliente','')}")
    c.drawString(m+97*mm, sy-9*mm,  f"Nombre: {d.get('entrega_nombre','')}")
    c.drawString(m, sy-18*mm, f"CC: {d.get('cc','')}")
    c.drawString(m+97*mm, sy-18*mm, f"CC: {d.get('entrega_cc','')}")

    c.showPage(); c.save(); buf.seek(0)
    return buf

# ──────────────────────────────────────────
#  ROUTES
# ──────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate/<doc_type>", methods=["POST"])
def generate(doc_type):
    data = request.get_json() or {}
    if doc_type == "orden-pedido":
        return send_file(pdf_orden(data), as_attachment=True, download_name="orden-pedido.pdf", mimetype="application/pdf")
    if doc_type == "acta-entrega":
        return send_file(pdf_acta(data), as_attachment=True, download_name="acta-entrega.pdf", mimetype="application/pdf")
    if doc_type == "cambio-producto":
        return send_file(pdf_cambio(data), as_attachment=True, download_name="cambio-producto.pdf", mimetype="application/pdf")
    return jsonify({"error": "Tipo inválido"}), 400

if __name__ == "__main__":
    app.run(debug=True)
