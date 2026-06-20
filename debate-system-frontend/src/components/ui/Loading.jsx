// src/components/ui/Loading.jsx
// ─────────────────────────────────────────────────────────────────────────────
// A DUMB (PRESENTATIONAL) component.
// It receives a 'message' prop and renders a loading indicator.
// It has NO state, NO API calls, NO side effects.
// It is a pure function: same props → same output, always.
// ─────────────────────────────────────────────────────────────────────────────

// Why a 'message' prop with a default value?
// Some loading states say "Starting debate..." and others say "Loading history..."
// The default covers cases where callers don't specify a message.
const Loading = ({ message = 'Loading...' }) => {
  return (
    // The wrapper div has role="status" for accessibility.
    // Screen readers announce "status" regions when their content changes.
    // aria-label gives screen readers something meaningful to say.
    <div
      role="status"
      aria-label={message}
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '3rem',
        gap: '1rem',
      }}
    >
      {/* The spinner is pure CSS — no library needed for a simple animation.
          It is a circle with one coloured segment that rotates.
          'border-top-color: #646cff' is the coloured segment.
          'animation: spin 0.8s linear infinite' rotates it forever. */}
      <div
        style={{
          width: '40px',
          height: '40px',
          border: '3px solid #e5e7eb',   // light grey full circle
          borderTopColor: '#646cff',      // purple segment (the "moving" part)
          borderRadius: '50%',
          animation: 'spin 0.8s linear infinite',
        }}
      />

      {/* The keyframes for the spin animation must be defined somewhere.
          In a real project you'd put this in index.css or a CSS module.
          Including here for completeness. */}
      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>

      <p style={{ color: '#6b7280', fontSize: '0.9rem', margin: 0 }}>
        {message}
      </p>
    </div>
  );
};

export default Loading;

// ─────────────────────────────────────────────────────────────────────────────
// USAGE EXAMPLES:
// <Loading />
// <Loading message="Starting your debate..." />
// <Loading message="Fetching history from database..." />
// ─────────────────────────────────────────────────────────────────────────────