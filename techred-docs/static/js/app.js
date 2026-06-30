const zone = document.getElementById("form-zone");
const buttons = document.querySelectorAll(".doc-btn");

const forms = {
  "orden-pedido": `
    <form id="doc-form">
      <div class="grid">
        <input name="cliente" placeholder="Cliente">
        <input name="cc" placeholder="C.C">
        <input name="tel" placeholder="Tel/Cel">
        <input name="direccion" placeholder="Dirección">
        <input name="barrio" placeholder="Barrio">
        <input name="ciudad" placeholder="Ciudad">
        <input name="contacto1" placeholder="Contacto 1">
        <input name="contacto2" placeholder="Contacto 2">
        <input name="correo" placeholder="Correo">
      </div>
      <button type="submit">Descargar PDF</button>
    </form>
  `
};

function render(doc) {
  zone.innerHTML = forms[doc] || "<p>Formulario pendiente.</p>";
  const form = document.getElementById("doc-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());

    const res = await fetch(`/generate/${doc}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${doc}.pdf`;
    a.click();
    URL.revokeObjectURL(url);
  });
}

buttons.forEach(btn => {
  btn.addEventListener("click", () => {
    buttons.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    render(btn.dataset.doc);
  });
});

render("orden-pedido");