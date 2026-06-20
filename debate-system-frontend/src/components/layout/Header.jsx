// FILE: src/components/layout/Header.jsx

function Header({ currentPage, onNavigate }) {
  // currentPage and onNavigate are props from App.jsx
  
  const navItems = [
    { id: 'home', label: 'Dashboard' },
    { id: 'debates', label: 'All Debates' },
    { id: 'create', label: 'New Debate' },
    { id: 'history', label: 'History' },
  ];
  
  return (
    <header className="header">
      <div className="header-brand">
        <h1>🤖 Multi-Agent Debate System</h1>
      </div>
      
      <nav className="header-nav">
        {navItems.map(item => (
          <button
            key={item.id}
            className={`nav-btn ${currentPage === item.id ? 'active' : ''}`}
            onClick={() => onNavigate(item.id)}
          >
            {item.label}
          </button>
        ))}
      </nav>
    </header>
  );
}

export default Header;