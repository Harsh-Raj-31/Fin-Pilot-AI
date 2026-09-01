function Topbar() {
  return (
    <header className="topbar">
      <div className="topbar-left">
        <span className="market-status">
          <span className="status-dot"></span>
          Live Market
        </span>
      </div>

      <div className="topbar-right">
        <div className="market-index">
          <span>NIFTY 50</span>
          <strong>24,541.15</strong>
          <span className="positive">+0.62%</span>
        </div>

        <button
          type="button"
          className="topbar-icon"
          aria-label="Notifications"
        >
          🔔
        </button>

        <button
          type="button"
          className="topbar-icon"
          aria-label="Theme"
        >
          ◐
        </button>
      </div>
    </header>
  )
}

export default Topbar