// src/hooks/useDebate.js
// ─────────────────────────────────────────────────────────────────────────────
// A custom hook is a plain JavaScript function that:
//   1. Starts with "use" (required by React's linting rules)
//   2. Calls other hooks (useState, useEffect, etc.)
//   3. Returns values the component needs
//
// Custom hooks are not magic — they are just functions.
// The "use" prefix signals to React and linters that this function
// follows hook rules (only call hooks at the top level, not inside
// loops or conditions).
//
// WHY extract to a hook?
// If HomePage has 200 lines of JSX and 100 lines of API logic mixed in,
// it becomes unreadable. Extracting the logic to useDebate() means:
//   - HomePage becomes pure JSX — easy to read, easy to style
//   - useDebate becomes pure logic — easy to test, easy to reuse
// ─────────────────────────────────────────────────────────────────────────────

import { useState } from 'react';
import { runDebate, getDebateHistory } from '../services/debateService.js';

// Returns an object with state values and handler functions.
// The component destructures exactly what it needs.
export const useDebate = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);

  const submitDebate = async (topic) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await runDebate(topic);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Debate failed');
    } finally {
      setLoading(false);
    }
  };

  const fetchHistory = async () => {
    setHistoryLoading(true);
    try {
      const data = await getDebateHistory();
      setHistory(data);
    } catch (err) {
      console.error('Failed to load history:', err);
    } finally {
      setHistoryLoading(false);
    }
  };

  // The hook returns everything the component might need.
  // The component only destructures what it actually uses.
  return {
    loading,
    error,
    result,
    history,
    historyLoading,
    submitDebate,
    fetchHistory,
  };
};