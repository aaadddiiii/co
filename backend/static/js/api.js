const API = async (url, method = "GET", body = null, json = false) => {
    const options = {
        method,
        credentials: "include"
    };

    if (body) {
        if (json) {
            options.headers = {
                "Content-Type": "application/json"
            };
            options.body = JSON.stringify(body);
        } else {
            options.body = body;
        }
    }

    let res;

    try {
        res = await fetch(url, options);
    } catch {
        alert("Network error. Check connection.");
        throw new Error("Network error");
    }

    // redirect (session expired etc.)
    if (res.redirected) {
        window.location.href = res.url;
        return;
    }

    // handle empty response
    if (res.status === 204) return;

    let data;

    try {
        data = await res.json();
    } catch {
        alert("Server returned invalid response.");
        throw new Error("Invalid JSON response");
    }

    if (!res.ok || !data.success) {
        const msg = data?.error || data?.message || "Request failed";
        alert(msg);
        throw new Error(msg);
    }

    return data.data;
};