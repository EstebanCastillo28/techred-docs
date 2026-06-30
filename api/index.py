import os
import json
import io
from flask import Flask, render_template, request, send_file, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

app = Flask(__name__, template_folder="../templates", static_folder="../static")

# IDs de las plantillas en Google Drive
DOC_IDS = {
    "acta-entrega":    "1GpIA_o9PKS2Y9t1EnNzM98QwV3hFVYqi",
    "cambio-producto": "1hepEdbtgXqFIJcLPpPHMj2imn5a_0s_5",
    "orden-pedido":    "TALONARIO_DOC_ID_PENDIENTE",  # reemplazar con el ID real
}

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]


def get_services():
    creds_json = os.environ.get("GOOGLE_CREDENTIALS")
    if not creds_json:
        raise RuntimeError("Variable GOOGLE_CREDENTIALS no configurada en Vercel")
    info = json.loads(creds_json)
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    drive = build("drive", "v3", credentials=creds)
    docs  = build("docs", "v1", credentials=creds)
    return drive, docs


def reemplazar_placeholders(docs_service, doc_id, reemplazos: dict):
    requests_list = []
    for placeholder, valor in reemplazos.items():
        requests_list.append({
            "replaceAllText": {
                "containsText": {
                    "text": "{{" + placeholder + "}}",
                    "matchCase": True,
                },
                "replaceText": str(valor) if valor else "",
            }
        })
    if requests_list:
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": requests_list},
        ).execute()


def generar_pdf(doc_type: str, datos: dict) -> io.BytesIO:
    drive, docs = get_services()
    template_id = DOC_IDS[doc_type]

    # 1. Copiar plantilla dentro del mismo Shared Drive
    copia = drive.files().copy(
        fileId=template_id,
        body={"name": f"temp_{doc_type}"},
        supportsAllDrives=True,
    ).execute()
    copia_id = copia["id"]

    try:
        # 2. Reemplazar placeholders
        reemplazar_placeholders(docs, copia_id, datos)

        # 3. Exportar como PDF
        request_export = drive.files().export_media(
            fileId=copia_id,
            mimeType="application/pdf",
        )
        buf = io.BytesIO()
        downloader = MediaIoBaseDownload(buf, request_export)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        buf.seek(0)
        return buf
    finally:
        # 4. Eliminar copia temporal siempre
        drive.files().delete(
            fileId=copia_id,
            supportsAllDrives=True,
        ).execute()


# ----------------------------------------
# RUTAS
# ----------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate/acta-entrega", methods=["POST"])
def gen_acta():
    d = request.get_json() or {}
    datos = {
        "cliente":         d.get("cliente", ""),
        "tipo_doc":        d.get("tipo_doc", ""),
        "cc":              d.get("cc", ""),
        "cuenta_contrato": d.get("cuenta_contrato", ""),
        "dia":             d.get("dia", ""),
        "mes":             d.get("mes", ""),
        "anio":            d.get("anio", ""),
        "consecutivo":     d.get("consecutivo", ""),
        "direccion":       d.get("direccion", ""),
        "desc_1":          d.get("desc_1", ""),
        "cant_1":          d.get("cant_1", ""),
        "valor_1":         d.get("valor_1", ""),
        "desc_2":          d.get("desc_2", ""),
        "cant_2":          d.get("cant_2", ""),
        "valor_2":         d.get("valor_2", ""),
        "desc_3":          d.get("desc_3", ""),
        "cant_3":          d.get("cant_3", ""),
        "valor_3":         d.get("valor_3", ""),
        "nombre_entrega":  d.get("nombre_entrega", ""),
        "cc_entrega":      d.get("cc_entrega", ""),
    }
    pdf = generar_pdf("acta-entrega", datos)
    return send_file(pdf, as_attachment=True,
                     download_name="acta-entrega.pdf",
                     mimetype="application/pdf")


@app.route("/generate/orden-pedido", methods=["POST"])
def gen_orden():
    d = request.get_json() or {}
    datos = {
        "cliente":          d.get("cliente", ""),
        "cc":               d.get("cc", ""),
        "tel":              d.get("tel", ""),
        "direccion":        d.get("direccion", ""),
        "barrio":           d.get("barrio", ""),
        "ciudad":           d.get("ciudad", ""),
        "contacto1":        d.get("contacto1", ""),
        "contacto2":        d.get("contacto2", ""),
        "correo":           d.get("correo", ""),
        "dia":              d.get("dia", ""),
        "mes":              d.get("mes", ""),
        "anio":             d.get("anio", ""),
        "cuenta_contrato":  d.get("cuenta_contrato", ""),
        "ref_1":            d.get("ref_1", ""),
        "cant_1":           d.get("cant_1", ""),
        "desc_1":           d.get("desc_1", ""),
        "valor_producto_1": d.get("valor_producto_1", ""),
        "cuotas_1":         d.get("cuotas_1", ""),
        "valor_cuotas_1":   d.get("valor_cuotas_1", ""),
        "ref_2":            d.get("ref_2", ""),
        "cant_2":           d.get("cant_2", ""),
        "desc_2":           d.get("desc_2", ""),
        "valor_producto_2": d.get("valor_producto_2", ""),
        "cuotas_2":         d.get("cuotas_2", ""),
        "valor_cuotas_2":   d.get("valor_cuotas_2", ""),
        "ref_3":            d.get("ref_3", ""),
        "cant_3":           d.get("cant_3", ""),
        "desc_3":           d.get("desc_3", ""),
        "valor_producto_3": d.get("valor_producto_3", ""),
        "cuotas_3":         d.get("cuotas_3", ""),
        "valor_cuotas_3":   d.get("valor_cuotas_3", ""),
        "ref_4":            d.get("ref_4", ""),
        "cant_4":           d.get("cant_4", ""),
        "desc_4":           d.get("desc_4", ""),
        "valor_producto_4": d.get("valor_producto_4", ""),
        "cuotas_4":         d.get("cuotas_4", ""),
        "valor_cuotas_4":   d.get("valor_cuotas_4", ""),
        "valor_total":      d.get("valor_total", ""),
        "forma_pago_otro":  d.get("forma_pago_otro", ""),
        "contraentrega":    d.get("contraentrega", ""),
        "asesor":           d.get("asesor", ""),
        "cod_asesor":       d.get("cod_asesor", ""),
        "supervisor":       d.get("supervisor", ""),
    }
    pdf = generar_pdf("orden-pedido", datos)
    return send_file(pdf, as_attachment=True,
                     download_name="orden-pedido.pdf",
                     mimetype="application/pdf")


@app.route("/generate/cambio-producto", methods=["POST"])
def gen_cambio():
    d = request.get_json() or {}
    datos = {
        "cliente":         d.get("cliente", ""),
        "cc":              d.get("cc", ""),
        "cuenta_contrato": d.get("cuenta_contrato", ""),
        "dia":             d.get("dia", ""),
        "mes":             d.get("mes", ""),
        "anio":            d.get("anio", ""),
        "producto_actual": d.get("producto_actual", ""),
        "producto_nuevo":  d.get("producto_nuevo", ""),
        "motivo":          d.get("motivo", ""),
        "nombre_entrega":  d.get("nombre_entrega", ""),
        "cc_entrega":      d.get("cc_entrega", ""),
    }
    pdf = generar_pdf("cambio-producto", datos)
    return send_file(pdf, as_attachment=True,
                     download_name="cambio-producto.pdf",
                     mimetype="application/pdf")


if __name__ == "__main__":
    app.run(debug=True)
