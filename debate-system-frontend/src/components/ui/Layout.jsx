// src/components/ui/Layout.jsx
// ─────────────────────────────────────────────────────────────────────────────
// Layout is a WRAPPER component that provides consistent structure to every page.
//
// THE CHILDREN PROP — this is fundamental to Component Composition.
// In React, any JSX you put between opening and closing tags of a component
// becomes available as props.children inside that component.
//
// <Layout>
//   <p>This is children</p>
// </Layout>
//
// Inside Layout.jsx: props.children === <p>This is children</p>
//
// This lets you wrap arbitrary content in a consistent shell (Navbar + footer)
// WITHOUT the shell needing to know anything about what it wraps.
// The Navbar is in Layout, so you never forget to add it to a page.
// ─────────────────────────────────────────────────────────────────────────────

import Navbar from './Navbar.jsx';

// Destructure children from props — same as { children } = props
const Layout = ({ children }) => {
  return (
    // The outermost div is the full page.
    <div style={{ minHeight: '100vh', backgroundColor: '#0a0a14' }}>

      {/* Navbar renders at the top of every page automatically */}
      <Navbar />

      {/* main is a semantic HTML5 element — screen readers find the primary content */}
      <main
        style={{
          maxWidth: '900px',
          margin: '0 auto',      // horizontally centres the content
          padding: '2rem 1.5rem',
        }}
      >
        {/* children renders whatever the page passed between <Layout> tags */}
        {children}
      </main>
    </div>
  );
};

export default Layout;