// src/components/ui/Navbar.jsx
// ─────────────────────────────────────────────────────────────────────────────
// A purely presentational navigation bar.
// In a real app you'd use React Router's <Link> here for client-side navigation.
// For now we use <a> tags as placeholders.
// ─────────────────────────────────────────────────────────────────────────────

const Navbar = () => {
  return (
    <nav
      role="navigation"
      aria-label="Main navigation"
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '1rem 2rem',
        backgroundColor: '#0f0f1a',
        borderBottom: '1px solid #1e1e3a',
        position: 'sticky',
        top: 0,
        zIndex: 100,
      }}
    >
      {/* Brand */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.75rem',
        }}
      >
        <span style={{ fontSize: '1.5rem' }}>⚖️</span>

        <span
          style={{
            color: 'white',
            fontWeight: '700',
            fontSize: '1.1rem',
            letterSpacing: '-0.02em',
          }}
        >
          Debate AI
        </span>
      </div>

      {/* Navigation Links */}
      <div
        style={{
          display: 'flex',
          gap: '2rem',
        }}
      >
        {[
          { href: '/', label: 'New Debate' },
          { href: '/history', label: 'History' },
        ].map(({ href, label }) => (
          <a
            key={href}
            href={href}
            style={{
              color: '#9ca3af',
              textDecoration: 'none',
              fontSize: '0.9rem',
              fontWeight: '500',
              transition: 'color 0.15s',
            }}
            onMouseEnter={(e) => {
              e.target.style.color = 'white';
            }}
            onMouseLeave={(e) => {
              e.target.style.color = '#9ca3af';
            }}
          >
            {label}
          </a>
        ))}
      </div>
    </nav>
  );
};

export default Navbar;