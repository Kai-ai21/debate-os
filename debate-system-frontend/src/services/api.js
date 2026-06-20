// src/services/api.js
// ─────────────────────────────────────────────────────────────────────────────
// This file configures the Axios HTTP client that your entire application uses.
// Think of it as setting up your "telephone" before any calls are made.
// ─────────────────────────────────────────────────────────────────────────────

import axios from 'axios';

// We read the base URL from environment variables.
// If the variable is missing, we fall back to localhost.
// This prevents silent failures in misconfigured environments.
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// axios.create() creates a pre-configured HTTP client instance.
// Every request made through this instance inherits these settings automatically.
// This is the Axios equivalent of a "configured fetch factory."
const api = axios.create({
  baseURL: BASE_URL,

  // Every request will wait 15 seconds before giving up.
  // Without this, failed requests hang forever if the server is down.
  timeout: 15000,

  // These headers are sent with every request.
  // 'Content-Type: application/json' tells FastAPI: "the body I'm sending is JSON."
  // 'Accept: application/json' tells FastAPI: "please respond with JSON."
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// ─────────────────────────────────────────────────────────────────────────────
// INTERCEPTORS — Middleware for HTTP requests and responses
// ─────────────────────────────────────────────────────────────────────────────
// Interceptors run before every request is sent and after every response arrives.
// They are the perfect place for cross-cutting concerns: auth tokens, logging,
// error transformation. The alternative is repeating this logic in every API call.

// REQUEST INTERCEPTOR
// This function runs right before every outgoing HTTP request.
api.interceptors.request.use(
  (config) => {
    // In a production app with authentication, you would read the JWT token
    // from localStorage here and attach it to every request:
    // const token = localStorage.getItem('authToken');
    // if (token) config.headers.Authorization = `Bearer ${token}`;

    // For debugging during development, log every outgoing request.
    // In production, you would remove this or gate it behind a debug flag.
    if (import.meta.env.DEV) {
      console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`, config.data);
    }
    return config;    // MUST return config or the request is cancelled
  },
  (error) => {
    // If something goes wrong BEFORE the request is sent (e.g., config error),
    // reject the promise so the calling code catches it.
    return Promise.reject(error);
  }
);

// RESPONSE INTERCEPTOR
// This function runs after every incoming HTTP response.
api.interceptors.response.use(
  (response) => {
    // A 2xx status code means success.
    // We return the response unchanged — callers will access response.data.
    return response;
  },
  (error) => {
    // Any non-2xx status code (400, 401, 403, 404, 500) lands here.
    // This is where you handle global error patterns.

    if (error.response?.status === 401) {
      // Token expired → redirect to login page
      // window.location.href = '/login';
      console.warn('[API] Unauthorized — redirect to login');
    }

    if (error.response?.status === 500) {
      // Server crash → you could show a global error notification here
      console.error('[API] Server error — backend may be down');
    }

    // Re-throw the error so individual callers can still handle it.
    // If you swallow the error here, callers have no way to know it failed.
    return Promise.reject(error);
  }
);

export default api;