const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";


/* =========================
   SCHEMES
   ========================= */

export async function getSchemes(params = {}) {
  const queryParams = new URLSearchParams();

  if (params.q) {
    queryParams.set("q", params.q);
  }

  if (params.category && params.category !== "All") {
    queryParams.set("category", params.category);
  }

  const queryString = queryParams.toString();

  const url = queryString
    ? `${API_BASE_URL}/schemes/?${queryString}`
    : `${API_BASE_URL}/schemes/`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Failed to fetch schemes");
  }

  const data = await response.json();

  return data.results;
}


export async function getScheme(id) {
  const response = await fetch(
    `${API_BASE_URL}/schemes/${id}/`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch scheme");
  }

  return response.json();
}


/* =========================
   CITIZEN AUTHENTICATION
   ========================= */

export async function requestOTP(mobile) {
  const response = await fetch(
    `${API_BASE_URL}/auth/request-otp/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        mobile,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error || "Unable to send OTP."
    );
  }

  return data;
}


export async function verifyOTP(mobile, otp) {
  const response = await fetch(
    `${API_BASE_URL}/auth/verify-otp/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        mobile,
        otp,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error || "Unable to verify OTP."
    );
  }

  return data;
}


/* =========================
   CITIZEN SESSION
   ========================= */

export function saveCitizenSession(data) {
  localStorage.setItem(
    "citizen_token",
    data.token
  );

  localStorage.setItem(
    "citizen",
    JSON.stringify(data.citizen)
  );
}


export function getCitizenToken() {
  return localStorage.getItem(
    "citizen_token"
  );
}


export function getCitizen() {
  const citizen = localStorage.getItem(
    "citizen"
  );

  if (!citizen) {
    return null;
  }

  try {
    return JSON.parse(citizen);
  } catch {
    return null;
  }
}


export function logoutCitizen() {
  localStorage.removeItem(
    "citizen_token"
  );

  localStorage.removeItem(
    "citizen"
  );
}


/* =========================
   APPLICATIONS
   ========================= */

export async function createApplication(
  schemeId,
  formData
) {
  const token = getCitizenToken();

  if (!token) {
    throw new Error(
      "Citizen authentication is required."
    );
  }

  const response = await fetch(
    `${API_BASE_URL}/applications/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",

        Authorization: `Token ${token}`,
      },

      body: JSON.stringify({
        scheme_id: schemeId,
        form_data: formData,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error ||
      "Unable to create application."
    );
  }

  return data;
}


export async function getMyApplications() {
  const token = getCitizenToken();

  if (!token) {
    throw new Error(
      "Citizen authentication is required."
    );
  }

  const response = await fetch(
    `${API_BASE_URL}/applications/mine/`,
    {
      method: "GET",

      headers: {
        Authorization: `Token ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error ||
      "Unable to fetch applications."
    );
  }

  return data;
}


export async function getApplication(
  applicationNumber
) {
  const token = getCitizenToken();

  if (!token) {
    throw new Error(
      "Citizen authentication is required."
    );
  }

  const response = await fetch(
    `${API_BASE_URL}/applications/${applicationNumber}/`,
    {
      method: "GET",

      headers: {
        Authorization: `Token ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error ||
      "Unable to fetch application."
    );
  }

  return data;
}


export async function updateApplication(
  applicationNumber,
  formData
) {
  const token = getCitizenToken();

  if (!token) {
    throw new Error(
      "Citizen authentication is required."
    );
  }

  const response = await fetch(
    `${API_BASE_URL}/applications/${applicationNumber}/`,
    {
      method: "PATCH",

      headers: {
        "Content-Type": "application/json",

        Authorization: `Token ${token}`,
      },

      body: JSON.stringify({
        form_data: formData,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error ||
      "Unable to update application."
    );
  }

  return data;
}


export async function submitApplication(
  applicationNumber,
  formData = null
) {
  const token = getCitizenToken();

  if (!token) {
    throw new Error(
      "Citizen authentication is required."
    );
  }

  const payload = formData ? { form_data: formData } : {};

  const response = await fetch(
    `${API_BASE_URL}/applications/${applicationNumber}/submit/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },

      body: JSON.stringify(payload),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error ||
      "Unable to submit application."
    );
  }

  return data;
}


/* =========================
   DOCUMENTS
   ========================= */

export async function uploadApplicationDocument(
  applicationNumber,
  documentType,
  file
) {
  const token = getCitizenToken();

  if (!token) {
    throw new Error("Citizen authentication is required.");
  }

  const formData = new FormData();
  formData.append("document_type", documentType);
  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/applications/${applicationNumber}/documents/`,
    {
      method: "POST",
      headers: {
        Authorization: `Token ${token}`,
      },
      body: formData,
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Unable to upload document.");
  }

  return data;
}


export async function getApplicationDocuments(applicationNumber) {
  const token = getCitizenToken();

  if (!token) {
    throw new Error("Citizen authentication is required.");
  }

  const response = await fetch(
    `${API_BASE_URL}/applications/${applicationNumber}/documents/`,
    {
      method: "GET",
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Unable to fetch documents.");
  }

  return data;
}


export async function deleteApplicationDocument(
  applicationNumber,
  documentId
) {
  const token = getCitizenToken();

  if (!token) {
    throw new Error("Citizen authentication is required.");
  }

  const response = await fetch(
    `${API_BASE_URL}/applications/${applicationNumber}/documents/${documentId}/`,
    {
      method: "DELETE",
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Unable to delete document.");
  }

  return data;
}


export async function downloadApplicationDocument(
  applicationNumber,
  documentId,
  fileName
) {
  const token = getCitizenToken();

  if (!token) {
    throw new Error("Citizen authentication is required.");
  }

  const response = await fetch(
    `${API_BASE_URL}/applications/${applicationNumber}/documents/${documentId}/download/`,
    {
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error("Unable to download document.");
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = fileName || "document";
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}


/* =========================
   PDF GENERATION & DOWNLOAD
   ========================= */

export async function downloadApplicationPdf(applicationNumber) {
  const token = getCitizenToken();

  if (!token) {
    throw new Error("Citizen authentication is required.");
  }

  const response = await fetch(
    `${API_BASE_URL}/applications/${applicationNumber}/pdf/`,
    {
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error("Unable to generate application PDF.");
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `Application_${applicationNumber}.pdf`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}


export async function downloadBlankFormPdf(schemeId, schemeTitle = "Scheme") {
  const response = await fetch(
    `${API_BASE_URL}/schemes/${schemeId}/blank-form-pdf/`
  );

  if (!response.ok) {
    throw new Error("Unable to download blank form PDF.");
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `Blank_Form_${schemeId}.pdf`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}


/* =========================
   NOTIFICATIONS
   ========================= */

export async function getNotifications() {
  const token = getCitizenToken();

  if (!token) {
    return { unread_count: 0, results: [] };
  }

  const response = await fetch(`${API_BASE_URL}/notifications/`, {
    headers: {
      Authorization: `Token ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Unable to fetch notifications.");
  }

  return response.json();
}


export async function markNotificationRead(notificationId) {
  const token = getCitizenToken();

  if (!token) {
    return;
  }

  await fetch(`${API_BASE_URL}/notifications/${notificationId}/read/`, {
    method: "PATCH",
    headers: {
      Authorization: `Token ${token}`,
    },
  });
}


export async function markAllNotificationsRead() {
  const token = getCitizenToken();

  if (!token) {
    return;
  }

  await fetch(`${API_BASE_URL}/notifications/mark-all-read/`, {
    method: "POST",
    headers: {
      Authorization: `Token ${token}`,
    },
  });
}


/* =========================
   DEMO REVIEW ACTIONS
   ========================= */

export async function demoVerifyAllDocuments(applicationNumber) {
  const token = getCitizenToken();

  if (!token) {
    throw new Error("Citizen authentication is required.");
  }

  const response = await fetch(
    `${API_BASE_URL}/applications/${applicationNumber}/demo-verify/`,
    {
      method: "POST",
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Unable to complete demo verification.");
  }

  return data;
}


export async function demoVerifyDocument(
  applicationNumber,
  documentId,
  status = "VERIFIED",
  remarks = "Verified by YojanaSaathi Demo Review"
) {
  const token = getCitizenToken();

  if (!token) {
    throw new Error("Citizen authentication is required.");
  }

  const response = await fetch(
    `${API_BASE_URL}/applications/${applicationNumber}/documents/${documentId}/verify/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
      body: JSON.stringify({ status, remarks }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Unable to verify document.");
  }

  return data;
}


/* =========================
   APPLICATION STATUS (Phase 4)
   ========================= */

export async function getApplicationStatus(applicationNumber) {
  const token = getCitizenToken();

  if (!token) {
    throw new Error("Citizen authentication is required.");
  }

  const response = await fetch(
    `${API_BASE_URL}/applications/${applicationNumber}/status/`,
    {
      method: "GET",
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Unable to fetch application status.");
  }

  return data;
}


/* =========================
   YOJANASAATHI AGENT DELEGATION
   ========================= */

export async function createAgentDelegation(durationHours = 24, scopes = null) {
  const token = getCitizenToken();

  if (!token) {
    throw new Error("Citizen authentication is required.");
  }

  const payload = { duration_hours: durationHours };
  if (scopes) {
    payload.scopes = scopes;
  }

  const response = await fetch(
    `${API_BASE_URL}/auth/agent-delegation/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
      body: JSON.stringify(payload),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Unable to create agent delegation.");
  }

  return data;
}


export async function getAgentDelegations() {
  const token = getCitizenToken();

  if (!token) {
    throw new Error("Citizen authentication is required.");
  }

  const response = await fetch(
    `${API_BASE_URL}/auth/agent-delegations/`,
    {
      method: "GET",
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Unable to fetch agent delegations.");
  }

  return data;
}


export async function revokeAgentDelegation(delegationId) {
  const token = getCitizenToken();

  if (!token) {
    throw new Error("Citizen authentication is required.");
  }

  const response = await fetch(
    `${API_BASE_URL}/auth/agent-delegation/${delegationId}/revoke/`,
    {
      method: "POST",
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Unable to revoke agent delegation.");
  }

  return data;
}


/* =========================
   API BASE URL
   ========================= */

export default API_BASE_URL;