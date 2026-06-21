import api from './api.js';
import { fetchEventSource } from '@microsoft/fetch-event-source';

const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const streamDebate = async (topic, callbacks) => {
  const {
    onStatus,
    onProponent,
    onCritic,
    onModerator,
    onSaved,
    onDone,
    onError,
  } = callbacks;

  await fetchEventSource(`${BASE_URL}/debate`, {
    method: 'POST',

    headers: {
      'Content-Type': 'application/json',
      Accept: 'text/event-stream',
    },

    body: JSON.stringify({
      decision: topic,
      context: '',
    }),

    async onopen(response) {
      if (!response.ok) {
        throw new Error(`Backend returned ${response.status}`);
      }
    },

    onmessage(msg) {
      let data;

      try {
        data = JSON.parse(msg.data);
      } catch {
        data = msg.data;
      }

      switch (msg.event) {
        case 'status':
          onStatus?.(data);
          break;

        case 'proponent':
          onProponent?.(data);
          break;

        case 'critic':
          onCritic?.(data);
          break;

        case 'moderator':
          onModerator?.(data);
          break;

        case 'saved':
          onSaved?.(data);
          break;

        case 'done':
          onDone?.(data);
          break;

        case 'error':
          onError?.(data);
          break;
      }
    },

    onerror(err) {
      console.error(err);
      onError?.(err.message || 'Connection failed');
    },
  });
};

export const getDebateHistory = async () => {
  const response = await api.get('/debates');
  return response.data;
};

export const getDebateById = async (id) => {
  const response = await api.get(`/debates/${id}`);
  return response.data;
};