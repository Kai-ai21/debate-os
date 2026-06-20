// src/components/ui/Error.jsx
// ─────────────────────────────────────────────────────────────────────────────
// Another DUMB component. It receives:
//   - message: string — what went wrong
//   - onRetry: function (optional) — callback when "Try Again" is clicked
//
// WHY an onRetry callback instead of putting retry logic here?
// This component has no idea HOW to retry. It doesn't know which API
// function failed. The parent that owns the failed state knows how to retry.
// So we accept a callback and call it when the button is clicked.
// This is "Inversion of Control" — the child says "tell me what to do"
// instead of deciding itself.
// ─────────────────────────────────────────────────────────────────────────────

const Error = ({ message = 'Something went wrong', onRetry }) => {
  return (
    <div
      role="alert"   // Tells screen readers: "this is an important announcement"
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: '2rem',
        gap: '1rem',
        backgroundColor: '#fef2f2',  // light red background
        border: '1px solid #fecaca', // red border
        borderRadius: '12px',
        margin: '1rem 0',
      }}
    >
      {/* The ⚠ character is a Unicode warning sign.
          In a real project you'd use an icon library (Lucide, Heroicons). */}
      <div style={{ fontSize: '2rem' }}>⚠</div>

      <p style={{ color: '#dc2626', fontWeight: '600', margin: 0 }}>
        Error
      </p>

      <p style={{ color: '#7f1d1d', textAlign: 'center', margin: 0 }}>
        {message}
      </p>

      {/* Conditional rendering: only show the retry button if a callback was provided.
          The {onRetry && <button>} pattern is a guard.
          If onRetry is undefined, the expression short-circuits to false (renders nothing).
          If onRetry is a function, it renders the button.
          Never put onClick={onRetry} on a button if onRetry might be undefined —
          that crashes when the user clicks. Always guard first. */}
      {onRetry && (
        <button
          onClick={onRetry}
          style={{
            padding: '0.5rem 1.5rem',
            backgroundColor: '#dc2626',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '0.9rem',
          }}
        >
          Try Again
        </button>
      )}
    </div>
  );
};

export default Error;