export default function Navbar({ activeView, onNavigate }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'upload', label: 'Upload Invoices', icon: '📄' },
    { id: 'analysis', label: 'Analysis', icon: '🧠' },
    { id: 'reports', label: 'Reports', icon: '📋' },
  ]

  return (
    <nav className="navbar" id="main-nav">
      <div className="navbar__brand">
        <span className="navbar__logo-icon">💱</span>
        <div>
          <div className="navbar__logo">SafariFX</div>
          <div className="navbar__subtitle">Frontier Market FX Intelligence</div>
        </div>
      </div>

      <div className="navbar__nav">
        {navItems.map(item => (
          <button
            key={item.id}
            id={`nav-${item.id}`}
            className={`navbar__link ${activeView === item.id ? 'navbar__link--active' : ''}`}
            onClick={() => onNavigate(item.id)}
          >
            <span>{item.icon}</span> {item.label}
          </button>
        ))}
      </div>

      <div className="navbar__badge">
        <span>⚡</span>
        Powered by Foundry IQ
      </div>
    </nav>
  )
}
