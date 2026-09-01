import { NavLink } from 'react-router-dom'

function Sidebar({ user, onLogout }) {
  const menuItems = [
    {
      label: 'Dashboard',
      path: '/',
      icon: '⌂',
    },
    {
      label: 'Market',
      path: '/market',
      icon: '📈',
    },
    {
      label: 'Watchlist',
      path: '/watchlist',
      icon: '☆',
    },
    {
      label: 'AI Signals',
      path: '/ai-signals',
      icon: '🤖',
    },
    {
      label: 'Paper Trading',
      path: '/paper-trading',
      icon: '💰',
    },
    {
      label: 'Backtesting',
      path: '/backtesting',
      icon: '📊',
    },
    {
      label: 'Portfolio',
      path: '/portfolio',
      icon: '💼',
    },
    {
      label: 'Analytics',
      path: '/analytics',
      icon: '📉',
    },
    {
      label: 'News',
      path: '/news',
      icon: '📰',
    },
    {
      label: 'Settings',
      path: '/settings',
      icon: '⚙',
    },
  ]

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-logo">F</div>

        <div>
          <h1>FINPILOT AI</h1>
          <p>Your AI Financial Copilot</p>
        </div>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `nav-item ${isActive ? 'active' : ''}`
            }
          >
            <span className="nav-icon">{item.icon}</span>
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-bottom">
        <div className="user-card">
          <div className="user-avatar">
            {user?.full_name?.charAt(0)?.toUpperCase() || 'U'}
          </div>

          <div className="user-info">
            <strong>{user?.full_name || 'FinPilot User'}</strong>
            <span>{user?.email || ''}</span>
          </div>
        </div>

        <button
          type="button"
          className="logout-button"
          onClick={onLogout}
        >
          <span>↪</span>
          Logout
        </button>
      </div>
    </aside>
  )
}

export default Sidebar