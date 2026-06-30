from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
import textwrap

app = Flask(__name__, template_folder="../templates", static_folder="../static")

RED   = colors.HexColor("#cc0000")
BLACK = colors.black
GRAY  = colors.HexColor("#555555")
LGRAY = colors.HexColor("#e0e0e0")

W, H = A4
ML = 15 * mm  # margen izquierdo
MR = W - 15 * mm  # margen derecho


def draw_logo(c, y_top):
    """Logo •TECHRED en la esquina superior izquierda"""
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(BLACK)
    c.drawString(ML, y_top, "•TECH")
    c.setFillColor(RED)
    c.drawString(ML + 30*mm, y_top, "RED•")
    c.setFillColor(BLACK)
    c.setFont("Helvetica", 7.5)
    c.drawString(ML, y_top - 6*mm,  "Tecnología  •  Infraestructura")
    c.setFont("Helvetica-Bold", 7)
    c.drawString(ML, y_top - 11*mm, "NIT. 900.866.525 -6")
    c.drawString(ML, y_top - 15*mm, "CLL 68 # 23-61 7 DE AGOSTO")
    c.drawString(ML, y_top - 19*mm, "CORREO: VANTILISTO@TECHRED.COM.CO")
    c.drawString(ML, y_top - 23*mm, "www.techred.com.co")


def draw_footer(c):
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(W/2, 22*mm,
        "Línea de servicio al cliente y garantías - WhatsApp: 302 5555083")
    c.drawCentredString(W/2, 17*mm,
        "correo electrónico: servicio.cliente@techred.com.co")
    c.setFillColor(BLACK)
    c.setFont("Helvetica", 7)
    c.drawCentredString(W/2, 12*mm,
        "Conozca más en www.techred.com.co/pages/politicas-de-privacidad")
    c.drawCentredString(W/2, 7*mm,
        "Aplican T&C. Comercializado por Techred S.A.S. © Techred S.A.S 2026")


def lf(c, label, val, x, y, lw=22*mm, fw=80*mm, sz=9):
    """Dibuja un label en negrita + valor + linea subrayada"""
    c.setFont("Helvetica-Bold", sz)
    c.setFillColor(BLACK)
    c.drawString(x, y, label)
    c.setFont("Helvetica", sz)
    c.drawString(x + lw, y, str(val or ""))
    c.setLineWidth(0.4)
    c.setStrokeColor(BLACK)
    c.line(x + lw - 0.5, y - 3, x + lw + fw, y - 3)


def wrap_cell(text, width_mm, font="Helvetica", size=8):
    """Devuelve texto con saltos de línea para caber en width_mm aprox"""
    chars = max(1, int(width_mm / 2.1))
    return "\n".join(textwrap.wrap(str(text or ""), chars))


# ─────────────────────────────────────────────────────────────────────────────
# 1. ORDEN DE PEDIDO
# ─────────────────────────────────────────────────────────────────────────────
def pdf_orden(d):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)

    draw_logo(c, H - 18*mm)

    # Caja ORDEN DE PEDIDO (arriba derecha)
    bx = W - 46*mm
    c.setLineWidth(1.5)
    c.setStrokeColor(RED)
    c.roundRect(bx, H - 32*mm, 31*mm, 20*mm, 3)
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(bx + 15.5*mm, H - 20*mm, "ORDEN DE")
    c.drawCentredString(bx + 15.5*mm, H - 27*mm, "PEDIDO")
    c.setFillColor(BLACK)
    c.setStrokeColor(BLACK)

    # --- Datos del cliente ---
    y = H - 42*mm
    lf(c, "CLIENTE:",    d.get("cliente"),   ML, y, 20*mm, W-ML*2-20*mm-1)
    y -= 10*mm
    lf(c, "C.C:",        d.get("cc"),        ML, y, 11*mm, 42*mm)
    lf(c, "TEL/CEL:",    d.get("tel"),       ML+55*mm, y, 19*mm, 60*mm)
    y -= 10*mm
    lf(c, "DIRECCIÓN:", d.get("direccion"), ML, y, 23*mm, W-ML*2-23*mm-1)
    y -= 10*mm
    lf(c, "BARRIO:",     d.get("barrio"),    ML, y, 16*mm, 52*mm)
    lf(c, "CIUDAD:",     d.get("ciudad"),    ML+70*mm, y, 16*mm, W-ML*2-70*mm-16*mm-1)
    y -= 10*mm
    lf(c, "CONTACTO 1:", d.get("contacto1"),ML, y, 27*mm, W-ML*2-27*mm-1)
    y -= 10*mm
    lf(c, "CONTACTO 2:", d.get("contacto2"),ML, y, 27*mm, W-ML*2-27*mm-1)
    y -= 10*mm
    lf(c, "CORREO:",     d.get("correo"),    ML, y, 17*mm, W-ML*2-17*mm-1)

    # --- Fecha y cuenta contrato (debajo del cliente) ---
    y -= 14*mm
    c.setFont("Helvetica-Bold", 9)
    c.drawString(ML, y, "FECHA DE PEDIDO")
    date_cfg = [("DIA",9*mm),("MES",9*mm),("AÑO",14*mm)]
    date_vals = [d.get("dia",""), d.get("mes",""), d.get("anio","")]
    dx = ML + 38*mm
    for (lbl, dw), val in zip(date_cfg, date_vals):
        c.setLineWidth(0.8)
        c.setStrokeColor(BLACK)
        c.roundRect(dx, y-8*mm, dw, 9*mm, 1.5)
        c.setFont("Helvetica-Bold", 6)
        c.drawCentredString(dx + dw/2, y-1.5*mm, lbl)
        c.setFont("Helvetica", 9)
        c.drawCentredString(dx + dw/2, y-6.5*mm, str(val))
        dx += dw + 2*mm

    c.setFont("Helvetica-Bold", 9)
    c.drawString(dx + 5*mm, y, "CUENTA CONTRATO")
    c.setLineWidth(0.8)
    c.roundRect(dx + 5*mm, y-8*mm, 38*mm, 9*mm, 1.5)
    c.setFont("Helvetica", 9)
    c.drawCentredString(dx + 24*mm, y-6.5*mm, str(d.get("cuenta_contrato","")))

    # --- Tabla de productos ---
    y -= 18*mm
    items = d.get("items", [])
    while len(items) < 4:
        items.append({})
    rows = [["REF","CANT","DESCRIPCION","VALOR\nPRODUCTO","CUOTAS","VALOR\nCUOTAS"]]
    for it in items[:4]:
        rows.append([
            it.get("ref",""), it.get("cant",""),
            wrap_cell(it.get("descripcion",""), 68),
            it.get("valor_producto",""), it.get("cuotas",""),
            it.get("valor_cuotas","")
        ])
    rows.append(["","","VALOR TOTAL DE LA COMPRA",f"$ {d.get('valor_total','')}","",""])

    col_w = [18*mm, 13*mm, 72*mm, 30*mm, 17*mm, 27*mm]
    tbl = Table(rows, colWidths=col_w, rowHeights=[9*mm]+[13*mm]*4+[9*mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),BLACK),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),8),
        ("GRID",(0,0),(-1,-1),0.5,BLACK),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("ALIGN",(2,1),(2,-2),"LEFT"),
        ("LEFTPADDING",(2,1),(2,-2),4),
        ("SPAN",(2,5),(3,5)),
        ("BACKGROUND",(0,5),(-1,5),BLACK),
        ("TEXTCOLOR",(0,5),(-1,5),colors.white),
        ("FONTNAME",(2,5),(3,5),"Helvetica-Bold"),
        ("ALIGN",(2,5),(3,5),"RIGHT"),
    ]))
    tbl.wrapOn(c, W, H)
    tbl.drawOn(c, ML, y - tbl._height)
    y -= tbl._height + 10*mm

    # --- Forma de pago ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(ML, y, "FORMA DE PAGO")
    pays = [("EFECTIVO:","efectivo"),("VANTI LISTO:","vanti_listo"),("OTRO:","otro")]
    px = ML
    y -= 10*mm
    for lbl, key in pays:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(px, y, lbl)
        c.setLineWidth(0.8)
        c.setStrokeColor(BLACK)
        c.rect(px + 28*mm, y-2*mm, 7*mm, 7*mm)
        if d.get(key):
            c.setFont("Helvetica-Bold", 11)
            c.drawCentredString(px + 31.5*mm, y+2.5*mm, "X")
        px += 44*mm

    y -= 13*mm
    lf(c, "CONTRAENTREGA: $", d.get("contraentrega"), ML, y, 40*mm, 55*mm)
    y -= 10*mm
    lf(c, "ASESOR:",           d.get("asesor"),       ML, y, 19*mm, 80*mm)
    y -= 10*mm
    lf(c, "COD ASESOR:",       d.get("cod_asesor"),   ML, y, 27*mm, 55*mm)
    lf(c, "SUPERVISOR:",       d.get("supervisor"),   ML+88*mm, y, 25*mm, 55*mm)

    # --- Huella + Firma ---
    y -= 20*mm
    c.setLineWidth(0.8)
    c.setStrokeColor(BLACK)
    c.roundRect(W/2 - 50*mm, y - 35*mm, 25*mm, 35*mm, 4)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(W/2 - 37.5*mm, y - 38*mm, "HUELLA CLIENTE")
    c.line(W/2 + 5*mm, y - 35*mm, W - ML, y - 35*mm)
    c.drawCentredString(W/2 + 30*mm, y - 39*mm, "FIRMA CLIENTE")

    draw_footer(c)
    c.showPage()
    c.save()
    buf.seek(0)
    return buf


# ─────────────────────────────────────────────────────────────────────────────
# 2. ACTA DE ENTREGA
# ─────────────────────────────────────────────────────────────────────────────
def pdf_acta(d):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)

    # Titulo
    c.setFont("Helvetica-Bold", 9.5)
    titulo = ("ACTA DE ENTREGA DE PRODUCTOS Y/O SERVICIOS TECHRED S.A.S, "
              "FINANCIADOS A TRAVÉS DE LA FACTURA DEL SERVICIO "
              "DE GAS NATURAL DOMICILIARIO ACTUALIZADA 10/02/2026 .")
    lines_t = textwrap.wrap(titulo, 95)
    ty = H - 15*mm
    for ln in lines_t:
        c.drawString(ML, ty, ln)
        ty -= 5.5*mm

    # Fecha y consecutivo
    ty -= 3*mm
    c.setFont("Helvetica-Bold", 9)
    c.drawString(ML, ty, "FECHA DE GENERACION Y CONSECUTIVO.")
    ty -= 8*mm

    date_cols = [
        ("D", d.get("dia","")),
        ("M", d.get("mes","")),
        ("A", d.get("anio","")),
    ]
    dcw = [(W - ML*2) / 3] * 3
    dtbl = Table([[v for _,v in date_cols]], colWidths=dcw, rowHeights=8*mm)
    dtbl.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.5,BLACK),
        ("FONTSIZE",(0,0),(-1,-1),9),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    dtbl.wrapOn(c, W, H)
    dtbl.drawOn(c, ML, ty - 8*mm)
    ty -= 11*mm

    cons_tbl = Table([[f"{d.get('consecutivo','')} DE TALONARIO"]], colWidths=[W-ML*2], rowHeights=8*mm)
    cons_tbl.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.5,BLACK),
        ("FONTSIZE",(0,0),(-1,-1),9),
        ("ALIGN",(0,0),(-1,-1),"LEFT"),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),4),
    ]))
    cons_tbl.wrapOn(c, W, H)
    cons_tbl.drawOn(c, ML, ty - 8*mm)
    ty -= 14*mm

    # Titulo acta
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(W/2, ty, "ACTA DE ENTREGA")
    ty -= 12*mm

    # Parrafo introductorio
    styles = getSampleStyleSheet()
    body_style = ParagraphStyle(
        "body", fontName="Helvetica", fontSize=9, leading=13,
        alignment=TA_JUSTIFY, spaceAfter=0
    )
    bold_style = ParagraphStyle(
        "bold", fontName="Helvetica-Bold", fontSize=9, leading=13
    )

    cliente  = d.get("cliente","___________")
    tipo_doc = d.get("tipo_documento","CC")
    cc       = d.get("cc","___________")
    cuenta   = d.get("cuenta_contrato","___________")
    direccion= d.get("direccion","___________")

    parrafo = (
        f'Con la firma del presente documento Yo <b>{cliente}</b>, mayor de edad, identificado '
        f'con tipo de documento {tipo_doc} número <b>{cc}</b>_ y número de cuenta de pago '
        f'(Recibo público Vanti) No. <b>{cuenta}</b> confirmo que he recibido a satisfacción '
        f'el producto y/o servicio adquirido a través del programa de financiación de alguna '
        f'de las distribuidoras del <b>Grupo Vanti</b> (Vanti S.A. ESP, Gas Natural Cundiboyacense '
        f'S.A. ESP, Gasoriente S.A. ESP y/o Gasnacer S.A. ESP) indicado en la siguiente tabla de '
        f'descripción, el cual fue entregado en la dirección'
    )
    p = Paragraph(parrafo, body_style)
    p.wrapOn(c, W - ML*2, H)
    p.drawOn(c, ML, ty - p.height)
    ty -= p.height + 5*mm

    c.setFont("Helvetica-Bold", 9)
    c.drawString(ML, ty, f"{direccion} de acuerdo a mi solicitud.")
    ty -= 10*mm

    # Tabla productos
    items = d.get("items", [])
    while len(items) < 7:
        items.append({})
    rows = [["DESCRIPCIÓN", "CANTIDAD", "VALOR"]]
    for it in items[:7]:
        rows.append([
            wrap_cell(it.get("descripcion",""), 95),
            it.get("cantidad",""),
            it.get("valor","")
        ])
    col_w = [W - ML*2 - 22*mm - 28*mm, 22*mm, 28*mm]
    tbl = Table(rows, colWidths=col_w, rowHeights=[8*mm]+[11*mm]*7)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),BLACK),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),8.5),
        ("GRID",(0,0),(-1,-1),0.5,BLACK),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("ALIGN",(0,1),(0,-1),"LEFT"),
        ("LEFTPADDING",(0,1),(0,-1),4),
    ]))
    tbl.wrapOn(c, W, H)
    tbl.drawOn(c, ML, ty - tbl._height)
    ty -= tbl._height + 8*mm

    # Pagina 2: politicas y firmas
    c.showPage()
    draw_logo(c, H - 18*mm)
    ty2 = H - 48*mm

    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(ML, ty2, "POLÍTICAS DE DEVOLUCIÓN Y GARANTIAS TECH RED S.A.")
    ty2 -= 8*mm

    politica = (
        "El plazo máximo para solicitar el cambio de productos son (5) días calendario, "
        "contados a partir de la fecha de la entrega del mismo; el producto debe estar en "
        "condiciones aptas para su venta (sin uso, sin armar, debe estar en el empaque original "
        "con sus respectivos manuales, catálogo, junto con todos sus accesorios y sus piezas "
        "principales y demás accesorios que hacen parte del producto), luego de verificadas estas "
        "condiciones, se decidirá sobre la aprobación o rechazo de la solicitud de cambio."
    )
    garantia = (
        "Todos los artículos comercializados nuevos por <b>TECH RED S.A.S.</b> cuentan con una "
        "garantía de un (1) año o trescientos sesenta y cinco (365) días calendario, contados "
        "a partir de la fecha de entrega, con excepción de los productos de movilidad eléctrica "
        "y/o productos exceptuados por la regulación colombiana, en el estatuto del consumidor, "
        "para hacer efectiva la garantía usted deberá comunicarse a SERVICIO AL CLIENTE: "
        "3025555083, o al correo electrónico vantilisto@techred.com.co"
    )
    cuotas_txt = (
        "Con la firma del presente documento manifiesto de forma clara y expresa a la fecha de la "
        "presente entrega entiendo y acepto el valor del producto y de las cuotas pactadas, número "
        "de cuotas, así mismo el valor del seguro de vida mensual que se paga junto con la cuota, "
        "se da por aceptado todo lo contenido en este documento."
    )
    firma_txt = (
        f"Para constancia, la presente acta de entrega se recibe a conformidad y se declara en "
        f"perfecto estado el equipo. Se firma en la ciudad de {d.get('ciudad','___________')}, "
        f"a los {d.get('dia','')} días del mes de {d.get('mes','')} del año {d.get('anio','')}."
    )

    bold_body = ParagraphStyle(
        "bbody", fontName="Helvetica-Bold", fontSize=9, leading=13,
        alignment=TA_JUSTIFY
    )
    norm_body = ParagraphStyle(
        "nbody", fontName="Helvetica", fontSize=9, leading=13,
        alignment=TA_JUSTIFY
    )

    for txt, sty in [
        (politica, bold_body),
        (garantia, norm_body),
        (cuotas_txt, norm_body),
        (firma_txt, norm_body),
    ]:
        p = Paragraph(txt, sty)
        p.wrapOn(c, W - ML*2, H)
        p.drawOn(c, ML, ty2 - p.height)
        ty2 -= p.height + 7*mm

    # Datos de firmantes (4 columnas: recibe | | entrega | )
    ty2 -= 5*mm
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(ML, ty2, "Datos de la persona que recibe")
    c.drawString(W/2 + 5*mm, ty2, "Datos de la persona que realiza la entrega")
    ty2 -= 20*mm
    fw = W/2 - ML - 10*mm
    for x_off, lbl_n, val_n, lbl_c, val_c in [
        (ML,        "Firma:",  "",  "Nombre:",  d.get("cliente","")),
        (W/2+5*mm,  "Firma:",  "",  "Nombre:",  d.get("entrega_nombre","")),
    ]:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x_off, ty2, lbl_n)
        c.line(x_off + 14*mm, ty2 - 1, x_off + fw, ty2 - 1)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x_off, ty2 - 12*mm, lbl_c)
        c.setFont("Helvetica", 9)
        c.drawString(x_off + 20*mm, ty2 - 12*mm, val_c)
        c.setLineWidth(0.4)
        c.line(x_off + 20*mm, ty2 - 13*mm, x_off + fw, ty2 - 13*mm)

    ty2 -= 24*mm
    lf(c, "CC:", d.get("cc",""),          ML,         ty2, 8*mm, 50*mm)
    lf(c, "CC:", d.get("entrega_cc",""), W/2+5*mm,   ty2, 8*mm, 50*mm)

    # Nota legal
    ty2 -= 14*mm
    nota = (
        "<b>NOTA LEGAL:</b> El diligenciamiento incompleto o indebido de este formato ocasionará "
        "demoras en el proceso e incluso la cancelación del mismo. De acuerdo con lo dispuesto en "
        "el artículo 14 de la Ley 890 de 2004, a partir del 1 de enero de 2005, quien falsifique "
        "un documento privado que pueda servir de prueba incurrirá, si lo usa, en prisión de "
        "dieciséis (16) a ciento ocho (108) meses."
    )
    pn = Paragraph(nota, ParagraphStyle("nota",fontName="Helvetica",fontSize=7.5,leading=11,alignment=TA_JUSTIFY))
    pn.wrapOn(c, W - ML*2, H)
    pn.drawOn(c, ML, ty2 - pn.height)

    draw_footer(c)
    c.showPage()
    c.save()
    buf.seek(0)
    return buf


# ─────────────────────────────────────────────────────────────────────────────
# 3. FORMATO DE CAMBIO DE PRODUCTO
# ─────────────────────────────────────────────────────────────────────────────
def pdf_cambio(d):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)

    draw_logo(c, H - 18*mm)

    # Titulo
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(W/2, H - 44*mm, "Formato de Cambio de Producto")

    # Fecha
    y = H - 58*mm
    c.setFont("Helvetica-Bold", 9)
    c.drawString(ML, y, "Bogotá:")
    lf(c, "Dia:",  d.get("dia",""),  ML+16*mm, y, 10*mm, 14*mm)
    lf(c, "Mes:",  d.get("mes",""),  ML+42*mm, y, 10*mm, 14*mm)
    lf(c, "Año:",  d.get("anio",""), ML+68*mm, y, 10*mm, 18*mm)

    # Datos cliente
    y -= 14*mm
    lf(c, "Nombre del Cliente:", d.get("cliente",""),       ML, y, 45*mm, W-ML*2-45*mm-1)
    y -= 10*mm
    lf(c, "Cuenta Contrato:",    d.get("cuenta_contrato",""),ML, y, 38*mm, W-ML*2-38*mm-1)

    # Productos
    y -= 14*mm
    c.setFont("Helvetica-Bold", 9)
    c.drawString(ML, y, "Producto Financiado (Actual):")
    y -= 5*mm
    c.setLineWidth(0.4)
    c.setStrokeColor(BLACK)
    c.line(ML, y, MR, y)
    y -= 6*mm
    c.setFont("Helvetica", 9)
    c.drawString(ML, y, str(d.get("producto_actual","")))
    c.line(ML, y-3, MR, y-3)
    y -= 10*mm

    c.setFont("Helvetica-Bold", 9)
    c.drawString(ML, y, "Producto a Cambiar:")
    y -= 5*mm
    c.line(ML, y, MR, y)
    y -= 6*mm
    c.setFont("Helvetica", 9)
    c.drawString(ML, y, str(d.get("producto_nuevo","")))
    c.line(ML, y-3, MR, y-3)
    y -= 10*mm

    c.setFont("Helvetica-Bold", 9)
    c.drawString(ML, y, "Motivo del Cambio:")
    y -= 5*mm
    motivo_lines = textwrap.wrap(str(d.get("motivo","")), 105)
    for _ in range(max(4, len(motivo_lines))):
        if motivo_lines:
            c.setFont("Helvetica", 9)
            c.drawString(ML, y, motivo_lines.pop(0))
        c.setLineWidth(0.4)
        c.line(ML, y - 3, MR, y - 3)
        y -= 9*mm

    # Separador
    y -= 5*mm
    c.setLineWidth(1)
    c.line(ML, y, MR, y)
    y -= 10*mm

    # Datos de firmantes
    c.setFont("Helvetica-Bold", 9)
    c.drawString(ML, y, "Datos de la persona que recibe")
    c.drawString(W/2 + 5*mm, y, "Datos de la persona que realiza la entrega")
    y -= 20*mm
    fw = W/2 - ML - 12*mm

    for x_off, nombre, cc in [
        (ML,       d.get("cliente",""),        d.get("cc","")),
        (W/2+5*mm, d.get("entrega_nombre",""), d.get("entrega_cc","")),
    ]:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x_off, y, "Firma:")
        c.setLineWidth(0.4)
        c.line(x_off + 16*mm, y - 1, x_off + fw, y - 1)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x_off, y - 12*mm, "Nombre:")
        c.setFont("Helvetica", 9)
        c.drawString(x_off + 20*mm, y - 12*mm, nombre)
        c.setLineWidth(0.4)
        c.line(x_off + 20*mm, y - 13*mm, x_off + fw, y - 13*mm)

    y -= 24*mm
    lf(c, "CC:", d.get("cc",""),          ML,       y, 8*mm, 50*mm)
    lf(c, "CC:", d.get("entrega_cc",""), W/2+5*mm, y, 8*mm, 50*mm)

    draw_footer(c)
    c.showPage()
    c.save()
    buf.seek(0)
    return buf


# ─────────────────────────────────────────────────────────────────────────────
# RUTAS
# ─────────────────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate/orden-pedido", methods=["POST"])
def gen_orden():
    return send_file(pdf_orden(request.get_json() or {}),
                     as_attachment=True, download_name="orden-pedido.pdf",
                     mimetype="application/pdf")

@app.route("/generate/acta-entrega", methods=["POST"])
def gen_acta():
    return send_file(pdf_acta(request.get_json() or {}),
                     as_attachment=True, download_name="acta-entrega.pdf",
                     mimetype="application/pdf")

@app.route("/generate/cambio-producto", methods=["POST"])
def gen_cambio():
    return send_file(pdf_cambio(request.get_json() or {}),
                     as_attachment=True, download_name="cambio-producto.pdf",
                     mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)
