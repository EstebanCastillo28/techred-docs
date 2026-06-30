from flask import Flask, render_template, request, send_file, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from io import BytesIO

app = Flask(__name__, template_folder="../templates", static_folder="../static")

def line(c, x1, y1, x2, y2):
    c.line(x1, y1, x2, y2)

def text(c, x, y, value, size=9, bold=False):
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    c.drawString(x, y, str(value or ""))

def order_pdf(data):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4
    m = 16 * mm

    text(c, m, h-20*mm, "TECHRED", 20, True)
    text(c, m, h-28*mm, "Tecnología e Infraestructura", 9)

    text(c, 82*mm, h-22*mm, "CLIENTE:", 9, True)
    text(c, 105*mm, h-22*mm, data.get("cliente"))
    line(c, 104*mm, h-24*mm, 185*mm, h-24*mm)

    text(c, 82*mm, h-31*mm, "C.C:", 9, True)
    text(c, 95*mm, h-31*mm, data.get("cc"))
    line(c, 94*mm, h-33*mm, 125*mm, h-33*mm)

    text(c, 130*mm, h-31*mm, "TEL/CEL:", 9, True)
    text(c, 150*mm, h-31*mm, data.get("tel"))
    line(c, 149*mm, h-33*mm, 195*mm, h-33*mm)

    text(c, 82*mm, h-40*mm, "DIRECCIÓN:", 9, True)
    text(c, 107*mm, h-40*mm, data.get("direccion"))
    line(c, 106*mm, h-42*mm, 195*mm, h-42*mm)

    text(c, 82*mm, h-49*mm, "BARRIO:", 9, True)
    text(c, 99*mm, h-49*mm, data.get("barrio"))
    line(c, 98*mm, h-51*mm, 140*mm, h-51*mm)

    text(c, 145*mm, h-49*mm, "CIUDAD:", 9, True)
    text(c, 163*mm, h-49*mm, data.get("ciudad"))
    line(c, 162*mm, h-51*mm, 195*mm, h-51*mm)

    text(c, 82*mm, h-58*mm, "CONTACTO 1:", 9, True)
    text(c, 108*mm, h-58*mm, data.get("contacto1"))
    line(c, 107*mm, h-60*mm, 195*mm, h-60*mm)

    text(c, 82*mm, h-67*mm, "CONTACTO 2:", 9, True)
    text(c, 108*mm, h-67*mm, data.get("contacto2"))
    line(c, 107*mm, h-69*mm, 195*mm, h-69*mm)

    text(c, 82*mm, h-76*mm, "CORREO:", 9, True)
    text(c, 100*mm, h-76*mm, data.get("correo"))
    line(c, 99*mm, h-78*mm, 195*mm, h-78*mm)

    c.rect(165*mm, h-27*mm, 30*mm, 9*mm)
    text(c, 169*mm, h-22.5*mm, "ORDEN DE PEDIDO", 8, True)

    c.showPage()
    c.save()
    buf.seek(0)
    return buf

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate/<doc_type>", methods=["POST"])
def generate(doc_type):
    data = request.get_json() or {}

    if doc_type == "orden-pedido":
        pdf = order_pdf(data)
        return send_file(pdf, as_attachment=True, download_name="orden-pedido.pdf", mimetype="application/pdf")

    return jsonify({"error": "Documento no soportado aún"}), 400

if __name__ == "__main__":
    app.run(debug=True)