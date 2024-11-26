var data = []

function obtenerDataProductos() {
    const requestOptions = {
        method: "GET",
    };
    fetch("http://127.0.0.1:5000/productos", requestOptions)
        .then((response) => response.json())
        .then((result) => data = result)
        .then(() => listarProductos())
        .catch((error) => console.error(error));
}

obtenerDataProductos();

function listarProductos() {
    const container = document.getElementById("reviews-container");
    container.innerHTML = "";

    data.forEach((item, index) => {
        const reviewElement = document.createElement("div");
        reviewElement.className = "col";
        reviewElement.id = `review-${index}`;

        const imageHTML = item.imagen
            ? `<img class="imagen-producto img-fluid rounded-start" src="${item.imagen}" alt="${item.nombre}">`
            : "";

        reviewElement.innerHTML = `
        <div class="card shadow-lg item-menu" data-bs-theme="dark">
            <div class="row g-0">
              <div class="col-md-4">${imageHTML}</div>
              <div class="col-md-8">
                <div class="card-body mb-4">
                  <h5 class="card-title">${item.nombre}</h5>
                  <p class="card-text">${item.descripcion}</p>
                  <div class="comments" id="comments-${index}">
                    ${item.comentarios.map((comment) => `
                    <div class="comment small">${comment}</div>`).join("")}
                  </div>
                  <div class="comment-box">
                    <input type="text" placeholder="Escribe un comentario..." class="form-control form-control-sm mb-2" id="comment-input-${index}">
                    <button class="btn btn-sm btn-info float-end" onclick="addComment(${index})">Comentar</button>
                  </div>
                </div>
              </div>
            </div>
        `;

        container.appendChild(reviewElement);
    });
}

function addComment(index) {
    const commentInput = document.getElementById(`comment-input-${index}`);
    const commentText = commentInput.value.trim();

    if (commentText) {
        commentInput.value = "";
        crearComentario(data[index].id, commentText);
    }
}

function crearComentario(idProducto, comentario) {
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "text/plain");
    const requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: comentario,
    };
    fetch(`http://127.0.0.1:5000/productos/${idProducto}/comentario`, requestOptions)
        .then((response) => obtenerDataProductos())
        .catch((error) => console.error(error));
}