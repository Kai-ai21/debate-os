// src/components/features/DebateHistory.jsx
// ─────────────────────────────────────────────────────────────────────────────
// A DUMB component that renders a list of past debates.
// It receives:
//   debates: array of debate objects
//   onSelect: function(debate) — called when a debate is clicked
//
// THREE STATES — always handle them all:
//   1. Loading (handled by parent via separate Loading component)
//   2. Empty   — debates.length === 0
//   3. Populated — debates.length > 0
// ─────────────────────────────────────────────────────────────────────────────

const DebateHistory = ({ debates, onSelect }) => {

  // EMPTY STATE — when the user has no debates yet.
  // Never show a blank page — guide the user on what to do next.
  // This is sometimes called an "empty state" or "zero state."
  if (!debates || debates.length === 0) {
    return (
      <div style={{
        textAlign: 'center',
        padding: '4rem 2rem',
        backgroundColor: '#1a1a2e',
        borderRadius: '12px',
        border: '1px dashed #2d2d4e',
      }}>
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>⚖️</div>
        <h3 style={{ color: '#9ca3af', margin: '0 0 0.5rem 0' }}>No debates yet</h3>
        <p style={{ color: '#6b7280', margin: 0 }}>
          Start your first debate to see your history here.
        </p>
      </div>
    );
  }

  // POPULATED STATE
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
      {/* .map() transforms each debate data object into a React element.
          This is the fundamental pattern for rendering lists.
          React needs the 'key' prop to efficiently update the list.
          Use debate.id (a stable database ID) — never use Math.random()
          as a key because it generates a NEW key on every render,
          forcing React to destroy and recreate every DOM node. */}
      {debates.map((debate) => (
        <div
          key={debate.id}
          onClick={() => onSelect(debate)}
          role="button"           // semantic role for non-button clickable elements
          tabIndex={0}            // makes it keyboard-focusable
          onKeyDown={(e) => {
            // Keyboard accessibility: Enter and Space should activate buttons
            if (e.key === 'Enter' || e.key === ' ') onSelect(debate);
          }}
          style={{
            padding: '1rem 1.25rem',
            backgroundColor: '#1a1a2e',
            border: '1px solid #2d2d4e',
            borderRadius: '10px',
            cursor: 'pointer',
            transition: 'border-color 0.15s, background-color 0.15s',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.borderColor = '#646cff';
            e.currentTarget.style.backgroundColor = '#1e1e38';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.borderColor = '#2d2d4e';
            e.currentTarget.style.backgroundColor = '#1a1a2e';
          }}
        >
          <div>
            {/* Truncate long topics with CSS — no JS string cutting needed.
                'textOverflow: ellipsis' shows "..." when text overflows.
                Requires 'overflow: hidden' and 'whiteSpace: nowrap' to work. */}
            <p style={{
              color: 'white',
              margin: '0 0 0.25rem 0',
              fontWeight: '500',
              maxWidth: '500px',
              overflow: 'hidden',
              whiteSpace: 'nowrap',
              textOverflow: 'ellipsis',
            }}>
              {debate.topic}
            </p>
            <p style={{ color: '#6b7280', margin: 0, fontSize: '0.8rem' }}>
              {new Date(debate.timestamp).toLocaleDateString('en-US', {
                month: 'short', day: 'numeric', year: 'numeric'
              })}
            </p>
          </div>

          {/* Confidence badge inline in the list item */}
          {debate.confidence_score && (
            <span style={{
              backgroundColor: '#22c55e22',
              color: '#22c55e',
              padding: '0.2rem 0.6rem',
              borderRadius: '999px',
              fontSize: '0.8rem',
              fontWeight: '600',
              flexShrink: 0,
            }}>
              {Math.round(debate.confidence_score * 100)}%
            </span>
          )}
        </div>
      ))}
    </div>
  );
};

export default DebateHistory;