// ================= BASE =================
async function request(url, method = "GET", body = null, isForm = false) {
  const options = {
    method,
    credentials: "include",
    headers: {}
  };

  if (body) {
    if (isForm) {
      options.body = body;
    } else {
      options.headers["Content-Type"] = "application/json";
      options.body = JSON.stringify(body);
    }
  }

  const res = await fetch(url, options);
  return res.json();
}

// ================= AUTH =================
const AuthAPI = {
  login: (formData) => request("/login", "POST", formData, true),
  logout: () => request("/logout", "POST")
};

// ================= USERS =================
const UserAPI = {
  getAll: () => request("/users"),

  create: (formData) =>
    request("/users/update", "POST", formData, true),

  delete: (id) => {
    const f = new FormData();
    f.append("id", id);
    return request("/users/delete", "POST", f, true);
  }
};

// ================= SCHEDULE =================
const ScheduleAPI = {
  getAll: () => request("/schedule/all"),

  create: (formData) =>
    request("/schedule/create", "POST", formData, true),

  update: (formData) =>
    request("/schedule/update", "POST", formData, true),

  delete: (id) => {
    const f = new FormData();
    f.append("id", id);
    return request("/schedule/delete", "POST", f, true);
  }
};

// ================= ATTENDANCE =================
const AttendanceAPI = {
  getStudents: (class_id, period) =>
    request(`/attendance/teacher/students?class_id=${class_id}&period=${period}`),

  mark: (data) =>
    request("/attendance/teacher/mark", "POST", data),

  getTeacherSelf: () =>
    request("/attendance/teacher/self"),

  getStudent: () =>
    request("/attendance/student"),

  getParent: () =>
    request("/attendance/parent"),

  getAdminStudents: () =>
    request("/attendance/admin/students"),

  getAdminTeachers: () =>
    request("/attendance/admin/teachers"),

  update: (formData) =>
    request("/attendance/admin/update", "POST", formData, true),

  delete: (id) => {
    const f = new FormData();
    f.append("id", id);
    return request("/attendance/admin/delete", "POST", f, true);
  }
};

// ================= FEES =================
const FeeAPI = {
  getStudent: () => request("/fees/student"),
  getParent: () => request("/fees/parent"),
  getAll: () => request("/fees/all"),

  create: (formData) =>
    request("/fees/create", "POST", formData, true),

  pay: (formData) =>
    request("/fees/pay", "POST", formData, true)
};

// ================= PAYMENTS =================
const PaymentAPI = {
  getAll: () => request("/fees/payments"),

  verify: (id) => {
    const f = new FormData();
    f.append("payment_id", id);
    return request("/fees/verify", "POST", f, true);
  }
};

// ================= SALARY =================
const SalaryAPI = {
  getAll: () => request("/salary/all"),
  getAdmin: () => request("/salary/admin"),

  approve: (id) => {
    const f = new FormData();
    f.append("payment_id", id);
    return request("/salary/approve", "POST", f, true);
  },

  pay: (id) => {
    const f = new FormData();
    f.append("payment_id", id);
    return request("/salary/pay", "POST", f, true);
  }
};

// ================= ACCOUNTS =================
const AccountAPI = {
  getAll: () => request("/accounts/all"),
  getSummary: () => request("/accounts/summary"),

  getMonthly: (month, year) =>
    request(`/accounts/monthly?month=${month}&year=${year}`),

  add: (formData) =>
    request("/accounts/add", "POST", formData, true)
};

// ================= ANALYTICS =================
const AnalyticsAPI = {
  getOverview: () => request("/analytics/overview"),
  getMonthlyTrend: () => request("/analytics/monthly-trend"),
  getDefaulters: () => request("/analytics/defaulters"),
  getTopTeachers: () => request("/analytics/top-teachers"),

  getDateRange: (start, end) =>
    request(`/analytics/date-range?start=${start}&end=${end}`)
};