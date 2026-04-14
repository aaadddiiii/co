(async function () {
  try {
    const res = await fetch("/attendance/teacher/self", {
      credentials: "include"
    });

    if (res.status === 401) {
      window.location.href = "/";
    }
  } catch (e) {
    window.location.href = "/";
  }
})();