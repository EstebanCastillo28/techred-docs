const zone    = document.getElementById("form-zone");
const btns    = document.querySelectorAll(".doc-btn");
const toast   = document.getElementById("toast");

function showToast() {
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 3000);
}

/* ──────────────────────────────────────
   TEMPLATES HTML
────────────────────────────────────── */
const templates = {

"acta-entrega": `
<form id="doc-form" novalidate>
  <p class="form-heading">Acta de Entrega VANTI</p>

  <p class="section-title">Fecha y consecutivo</p>
  <div class="grid-4">
    <div class="field"><label>Día</label><input name="dia" placeholder="DD"></div>
    <div class="field"><label>Mes</label><input name="mes" placeholder="MM"></div>
    <div class="field"><label>Año</label><input name="anio" placeholder="AAAA"></div>
    <div class="field"><label>Consecutivo talonario</label><input name="consecutivo"></div>
  </div>

  <p class="section-title">Datos del cliente</p>
  <div class="grid-2">
    <div class="field"><label>Nombre completo</label><input name="cliente" required></div>
    <div class="field"><label>Tipo de documento</label>
      <select name="tipo_documento">
        <option value="CC">Cédula de Ciudadanía (CC)</option>
        <option value="CE">Cédula de Extranjería (CE)</option>
        <option value="NIT">NIT</option>
        <option value="PP">Pasaporte</option>
      </select>
    </div>
    <div class="field"><label>Número de documento</label><input name="cc"></div>
    <div class="field"><label>Cuenta contrato (Recibo Vanti)</label><input name="cuenta_contrato"></div>
    <div class="field col-2"><label>Dirección de entrega</label><input name="direccion"></div>
    <div class="field"><label>Ciudad</label><input name="ciudad"></div>
  </div>

  <p class="section-title">Quien realiza la entrega</p>
  <div class="grid-2">
    <div class="field"><label>Nombre</label><input name="entrega_nombre"></div>
    <div class="field"><label>Cédula</label><input name="entrega_cc"></div>
  </div>

  <p class="section-title">Detalle de productos (hasta 7 filas)</p>
  <div class="items-box">
    <div class="items-header acta-cols">
      <span>Descripción</span><span>Cantidad</span><span>Valor</span>
    </div>
    ${Array.from({length:7},(_,i)=>`
      <div class="item-row acta-cols">
        <input placeholder="Descripción del producto" data-g="items" data-i="${i}" data-k="descripcion">
        <input placeholder="0" data-g="items" data-i="${i}" data-k="cantidad">
        <input placeholder="$ 0" data-g="items" data-i="${i}" data-k="valor">
      </div>`).join("")}
  </div>

  <div class="btn-row">
    <button type="submit" class="btn btn-primary">⬇ Descargar PDF</button>
  </div>
</form>`,

"orden-pedido": `
<form id="doc-form" novalidate>
  <p class="form-heading">Orden de pedido</p>

  <p class="section-title">Datos del cliente</p>
  <div class="grid-2">
    <div class="field"><label>Nombre del cliente</label><input name="cliente" required></div>
    <div class="field"><label>C.C</label><input name="cc"></div>
    <div class="field"><label>Tel / Cel</label><input name="tel"></div>
    <div class="field col-2"><label>Dirección</label><input name="direccion"></div>
    <div class="field"><label>Barrio</label><input name="barrio"></div>
    <div class="field"><label>Ciudad</label><input name="ciudad"></div>
    <div class="field"><label>Contacto 1</label><input name="contacto1"></div>
    <div class="field"><label>Contacto 2</label><input name="contacto2"></div>
    <div class="field col-2"><label>Correo electrónico</label><input name="correo" type="email"></div>
  </div>

  <p class="section-title">Fecha y cuenta</p>
  <div class="grid-4">
    <div class="field"><label>Día</label><input name="dia" placeholder="DD"></div>
    <div class="field"><label>Mes</label><input name="mes" placeholder="MM"></div>
    <div class="field"><label>Año</label><input name="anio" placeholder="AAAA"></div>
    <div class="field"><label>Cuenta contrato</label><input name="cuenta_contrato"></div>
  </div>

  <p class="section-title">Detalle de productos (hasta 4 filas)</p>
  <div class="items-box">
    <div class="items-header order-cols">
      <span>REF</span><span>CANT</span><span>Descripción</span>
      <span>Valor producto</span><span>Cuotas</span><span>Valor cuota</span>
    </div>
    ${Array.from({length:4},(_,i)=>`
      <div class="item-row order-cols">
        <input placeholder="Ref" data-g="items" data-i="${i}" data-k="ref">
        <input placeholder="1" data-g="items" data-i="${i}" data-k="cant">
        <input placeholder="Descripción" data-g="items" data-i="${i}" data-k="descripcion">
        <input placeholder="$ 0" data-g="items" data-i="${i}" data-k="valor_producto">
        <input placeholder="0" data-g="items" data-i="${i}" data-k="cuotas">
        <input placeholder="$ 0" data-g="items" data-i="${i}" data-k="valor_cuotas">
      </div>`).join("")}
  </div>

  <p class="section-title">Totales y pago</p>
  <div class="grid-2">
    <div class="field"><label>Valor total de la compra</label><input name="valor_total" placeholder="$ 0"></div>
    <div class="field"><label>Contraentrega $</label><input name="contraentrega"></div>
  </div>
  <div class="field">
    <label>Forma de pago</label>
    <div class="pay-group">
      <label class="pay-option"><input type="checkbox" name="efectivo"> Efectivo</label>
      <label class="pay-option"><input type="checkbox" name="vanti_listo"> Vanti Listo</label>
      <label class="pay-option"><input type="checkbox" name="otro"> Otro</label>
    </div>
  </div>

  <p class="section-title">Datos del asesor</p>
  <div class="grid-2">
    <div class="field"><label>Asesor</label><input name="asesor"></div>
    <div class="field"><label>Código asesor</label><input name="cod_asesor"></div>
    <div class="field"><label>Supervisor</label><input name="supervisor"></div>
  </div>

  <div class="btn-row">
    <button type="submit" class="btn btn-primary">⬇ Descargar PDF</button>
  </div>
</form>`,

"cambio-producto": `
<form id="doc-form" novalidate>
  <p class="form-heading">Formato de cambio de producto</p>

  <p class="section-title">Fecha</p>
  <div class="grid-3">
    <div class="field"><label>Día</label><input name="dia" placeholder="DD"></div>
    <div class="field"><label>Mes</label><input name="mes" placeholder="MM"></div>
    <div class="field"><label>Año</label><input name="anio" placeholder="AAAA"></div>
  </div>

  <p class="section-title">Datos del cliente</p>
  <div class="grid-2">
    <div class="field"><label>Nombre completo</label><input name="cliente" required></div>
    <div class="field"><label>Cédula</label><input name="cc"></div>
    <div class="field"><label>Cuenta contrato</label><input name="cuenta_contrato"></div>
  </div>

  <p class="section-title">Productos</p>
  <div class="field">
    <label>Producto financiado (actual)</label>
    <textarea name="producto_actual" placeholder="Descripción del producto actual..."></textarea>
  </div>
  <div class="field">
    <label>Producto a cambiar</label>
    <textarea name="producto_nuevo" placeholder="Descripción del producto nuevo..."></textarea>
  </div>
  <div class="field">
    <label>Motivo del cambio</label>
    <textarea name="motivo" style="min-height:120px" placeholder="Describa el motivo del cambio..."></textarea>
  </div>

  <p class="section-title">Quien realiza la entrega</p>
  <div class="grid-2">
    <div class="field"><label>Nombre</label><input name="entrega_nombre"></div>
    <div class="field"><label>Cédula</label><input name="entrega_cc"></div>
  </div>

  <div class="btn-row">
    <button type="submit" class="btn btn-primary">⬇ Descargar PDF</button>
  </div>
</form>`
};

/* ──────────────────────────────────────
   RENDER & BIND
────────────────────────────────────── */
function render(doc) {
  zone.innerHTML = templates[doc] || "<p>Formulario no disponible.</p>";
  const form = document.getElementById("doc-form");
  if (!form) return;

  form.addEventListener("submit", async e => {
    e.preventDefault();
    const btn = form.querySelector("[type=submit]");
    btn.textContent = "Generando…";
    btn.disabled = true;

    const fd   = new FormData(form);
    const data = {};

    // Campos planos
    for (const [k, v] of fd.entries()) {
      if (form.querySelector(`[name="${k}"]`)?.type !== "checkbox") data[k] = v;
    }
    // Checkboxes
    form.querySelectorAll("input[type=checkbox]").forEach(cb => {
      data[cb.name] = cb.checked;
    });
    // Items agrupados
    const groups = {};
    form.querySelectorAll("[data-g='items']").forEach(inp => {
      const idx = Number(inp.dataset.i);
      const key = inp.dataset.k;
      groups[idx] = groups[idx] || {};
      groups[idx][key] = inp.value;
    });
    if (Object.keys(groups).length) data.items = Object.values(groups);

    try {
      const res  = await fetch(`/generate/${doc}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      const blob = await res.blob();
      const url  = URL.createObjectURL(blob);
      const a    = document.createElement("a");
      a.href = url;
      a.download = `${doc}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
      showToast();
    } catch (err) {
      alert("Error generando el PDF. Revisa la conexión al servidor.");
    } finally {
      btn.textContent = "⬇ Descargar PDF";
      btn.disabled = false;
    }
  });
}

btns.forEach(b => b.addEventListener("click", () => {
  btns.forEach(x => x.classList.remove("active"));
  b.classList.add("active");
  render(b.dataset.doc);
}));

render("acta-entrega");
