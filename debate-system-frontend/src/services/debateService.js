// src/services/debateService.js
// ─────────────────────────────────────────────────────────────────────────────
// This file contains all debate-related API calls.
// It imports the configured Axios instance from api.js.
// Components import from HERE — never from api.js directly.
// ─────────────────────────────────────────────────────────────────────────────

import api from './api.js';

// ─────────────────────────────────────────────────────────────────────────────
// runDebate — POST /run-debate
// ─────────────────────────────────────────────────────────────────────────────
// Sends a debate topic to the AI backend.
// Returns the full debate result including proponent, critic, and verdict.
//
// WHY async/await instead of .then()/.catch()?
// async/await produces flat, readable code. The same logic with .then() chains
// becomes nested and harder to follow. Both are equally correct — async/await
// is the modern preference for readability.
// ─────────────────────────────────────────────────────────────────────────────
export const runDebate = async (topic) => {
  // api.post(url, data) sends a POST request with the data as the JSON body.
  // Axios automatically serialises the object to JSON — you do NOT call JSON.stringify.
  // The response object has a .data property which is the parsed JSON body.
  const response = await api.post('/run-debate', { topic });

  // We return only response.data — the actual payload from FastAPI.
  // Components never need to know about HTTP response metadata (status codes, headers).
  return response.data;
};

// ─────────────────────────────────────────────────────────────────────────────
// getDebateHistory — GET /debates
// ─────────────────────────────────────────────────────────────────────────────
// Fetches the list of all past debates from PostgreSQL (via FastAPI).
// ─────────────────────────────────────────────────────────────────────────────
export const getDebateHistory = async () => {
  const response = await api.get('/debates');
  return response.data;
};

// ─────────────────────────────────────────────────────────────────────────────
// getDebateById — GET /debates/:id
// ─────────────────────────────────────────────────────────────────────────────
// Fetches a single debate by its ID for the detail view.
// ─────────────────────────────────────────────────────────────────────────────
export const getDebateById = async (id) => {
  const response = await api.get(`/debates/${id}`);
  return response.data;
};