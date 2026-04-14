function el(id) {
  return document.getElementById(id);
}

function renderList(containerId, items, renderFn) {
  let html = "";
  items.forEach(item => {
    html += renderFn(item);
  });
  el(containerId).innerHTML = html;
}

function formDataFrom(obj) {
  const f = new FormData();
  for (let key in obj) {
    f.append(key, obj[key]);
  }
  return f;
}