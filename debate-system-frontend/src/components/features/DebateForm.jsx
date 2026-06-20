// src/components/features/DebateForm.jsx
// ─────────────────────────────────────────────────────────────────────────────
// This component is partially "smart" — it manages form input state.
// But it does NOT make API calls. It delegates that to its parent (HomePage)
// via the onSubmit callback prop.
//
// WHY? If DebateForm called runDebate() directly:
//   1. The result would land inside DebateForm's state.
//   2. DebateResult couldn't access that result (sibling, not child).
//   3. You'd need to "thread" data upward — which is impossible with pure downward props.
//
// By lifting the API call to the parent (HomePage), the parent owns the result
// and can pass it to BOTH DebateForm (to clear the form) AND DebateResult (to display it).
// This is "Lifting State Up" — one of the most important React patterns.
// ─────────────────────────────────────────────────────────────────────────────

import { useState } from 'react';

// Props:
//   onSubmit(topic) — called when form is submitted with the topic string
//   isLoading — disables the form while a debate is running
const DebateForm = ({ onSubmit, isLoading }) => {

  // LOCAL STATE — form input is inherently local to this form.
  // The parent does not need to know what the user is CURRENTLY typing.
  // Only the final submitted value matters to the parent.
  // Rule: if only one component needs a piece of state, put it there.
  const [topic, setTopic] = useState('');

  // Form submission handler
  const handleSubmit = (event) => {
    // Prevent the browser's default form submission (page reload).
    // React handles routing and data submission — never let the browser do it.
    event.preventDefault();

    // Guard: don't submit empty or whitespace-only topics.
    // .trim() removes leading/trailing spaces before checking length.
    if (!topic.trim()) return;

    // Delegate to the parent. The parent will call runDebate(topic).
    // After submitting, optionally clear the form:
    // setTopic('');  ← uncomment if you want the field to clear on submit
    onSubmit(topic.trim());
  };

  return (
    // onSubmit on the <form> element handles both button click AND Enter key.
    // If you put onClick on the button only, pressing Enter doesn't submit.
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>

      <div>
        <label
          htmlFor="topic-input"   // htmlFor links the label to the input by ID
          style={{ display: 'block', marginBottom: '0.5rem', color: '#9ca3af', fontSize: '0.85rem', fontWeight: '600', letterSpacing: '0.05em', textTransform: 'uppercase' }}
        >
          Debate Topic
        </label>

        {/* CONTROLLED INPUT — React owns the value, not the DOM.
            value={topic} binds the input's displayed value to React state.
            onChange={(e) => setTopic(e.target.value)} updates state on every keystroke.
            Without value={topic}, React cannot predict what's in the input.
            Without onChange, the input becomes read-only (React controls it but won't update).
            This is the difference between CONTROLLED and UNCONTROLLED inputs. */}
        <input
          id="topic-input"
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="e.g. Should AI systems have legal rights?"
          disabled={isLoading}  // prevents typing while debate is running

          // When isLoading is true, the cursor becomes 'not-allowed' as visual feedback
          style={{
            width: '100%',
            padding: '0.9rem 1rem',
            backgroundColor: '#1a1a2e',
            border: '1px solid #2d2d4e',
            borderRadius: '10px',
            color: 'white',
            fontSize: '1rem',
            outline: 'none',
            boxSizing: 'border-box',
            cursor: isLoading ? 'not-allowed' : 'text',
            opacity: isLoading ? 0.6 : 1,
            transition: 'border-color 0.15s',
          }}
          onFocus={(e) => { if (!isLoading) e.target.style.borderColor = '#646cff'; }}
          onBlur={(e) => { e.target.style.borderColor = '#2d2d4e'; }}
        />
      </div>

      <button
        type="submit"

        // Disable when loading OR when topic is empty (guards both states)
        disabled={isLoading || !topic.trim()}

        style={{
          padding: '0.85rem 2rem',
          backgroundColor: isLoading ? '#374151' : '#646cff',  // grey when loading
          color: 'white',
          border: 'none',
          borderRadius: '10px',
          fontSize: '1rem',
          fontWeight: '600',
          cursor: isLoading || !topic.trim() ? 'not-allowed' : 'pointer',
          transition: 'background-color 0.15s',
          alignSelf: 'flex-start',
        }}
      >
        {/* Ternary conditional rendering — show different text based on state.
            This is cleaner than an if/else inside JSX for simple text swaps. */}
        {isLoading ? '⏳ Running Debate...' : '⚖️ Start Debate'}
      </button>
    </form>
  );
};

export default DebateForm;