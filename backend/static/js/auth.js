async function login() {
  const form = new FormData();
  form.append("email", document.getElementById("email").value);
  form.append("password", document.getElementById("password").value);

  const res = await AuthAPI.login(form);

  if (!res.success) {
    alert(res.error || "Login failed");
    return;
  }

  window.location.href = "/";
}

async function logout() {
  await AuthAPI.logout();
  window.location.href = "/";
}