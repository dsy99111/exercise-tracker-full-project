// --------- BASE URL ---------
const API = "http://127.0.0.1:8000/api/";


// --------- AUTH HEADERS ---------
function authHeaders() {
    const token = localStorage.getItem("token");

    return token
        ? {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`,
        }
        : {
            "Content-Type": "application/json"
        };
}


// --------- RESPONSE HANDLER ---------
async function handleResponse(res) {
    const data = await res.json();
    if (!res.ok) throw data;
    return data;
}



// ====================== AUTH ======================

// POST /api/auth/login/
export async function login(username, password) {
    const res = await fetch(API + "auth/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await handleResponse(res);

    // Save JWT access token
    if (data.token) {
        localStorage.setItem("token", data.token);
        localStorage.setItem("refresh", data.refresh);
        localStorage.setItem("username", data.username);
        localStorage.setItem("role", data.role);
        localStorage.setItem("userId", data.id);
    }

    return data;
}



// ====================== CONFIG ======================

// GET /api/config/
export async function getConfig() {
    return handleResponse(
        await fetch(API + "config/", {
            method: "GET",
            headers: authHeaders(),
        })
    );
}


// PUT /api/config/<pk>/
export async function updateConfig(key, value) {
    return handleResponse(
        await fetch(API + `config/${key}/`, {
            method: "PUT",
            headers: authHeaders(),
            body: JSON.stringify({ key, value }),
        })
    );
}



// ====================== USERS ======================

// GET /api/users/
export async function getUsers() {
    return handleResponse(
        await fetch(API + "users/", {
            method: "GET",
            headers: authHeaders(),
        })
    );
}


// POST /api/users/
export async function addUser(userData) {
    return handleResponse(
        await fetch(API + "users/", {
            method: "POST",
            headers: authHeaders(),
            body: JSON.stringify(userData),
        })
    );
}



// ====================== PROGRESS ======================

// GET /api/progress/
export async function getAllProgress() {
    return handleResponse(
        await fetch(API + "progress/", {
            method: "GET",
            headers: authHeaders(),
        })
    );
}


// POST /api/progress/
export async function addProgress(data) {

    // FIX 1: challenge must be string for Django model
    if (data.challenge) {
        data.challenge = String(data.challenge);
    }

    // FIX 2: Django expects param1..param5, not p1..p5
    if (data.p1) data.param1 = data.p1;
    if (data.p2) data.param2 = data.p2;
    if (data.p3) data.param3 = data.p3;
    if (data.p4) data.param4 = data.p4;
    if (data.p5) data.param5 = data.p5;

    return handleResponse(
        await fetch(API + "progress/", {
            method: "POST",
            headers: authHeaders(),
            body: JSON.stringify(data),
        })
    );
}



// PUT /api/progress/<id>/
export async function updateProgress(id, data) {
    return handleResponse(
        await fetch(API + `progress/${id}/`, {
            method: "PUT",
            headers: authHeaders(),
            body: JSON.stringify(data),
        })
    );
}


// DELETE /api/progress/<id>/
export async function deleteProgress(id) {
    return handleResponse(
        await fetch(API + `progress/${id}/`, {
            method: "DELETE",
            headers: authHeaders(),
        })
    );
}
export async function getRoutineHistory(uid) {
  const token = localStorage.getItem("token");

  const res = await fetch(`http://127.0.0.1:8000/api/routine-history/${uid}/`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  return res.json();
}


export async function saveRoutineAPI(payload) {
  const token = localStorage.getItem("token");

  const res = await fetch("http://127.0.0.1:8000/api/save-routine/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  });

  return res.json();
}
