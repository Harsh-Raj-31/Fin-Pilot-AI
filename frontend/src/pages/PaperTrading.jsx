import { useMemo, useState } from 'react'

/* =========================================================
   PAPER TRADING DATA
   ========================================================= */

const INITIAL_POSITIONS = [
  {
    symbol: 'HDFCBANK',
    quantity: 10,
    averagePrice: 1723.5,
    currentPrice: 1785.2,
    pnl: 617,
    pnlPercentage: 3.58,
  },
  {
    symbol: 'TCS',
    quantity: 7,
    averagePrice: 3645.2,
    currentPrice: 3812.45,
    pnl: 1170.75,
    pnlPercentage: 4.59,
  },
  {
    symbol: 'RELIANCE',
    quantity: 5,
    averagePrice: 2946.8,
    currentPrice: 3052.1,
    pnl: 526.5,
    pnlPercentage: 3.57,
  },
  {
    symbol: 'INFY',
    quantity: 8,
    averagePrice: 1512.4,
    currentPrice: 1548.75,
    pnl: 290.8,
    pnlPercentage: 2.4,
  },
  {
    symbol: 'SBIN',
    quantity: 12,
    averagePrice: 812.35,
    currentPrice: 798.2,
    pnl: -169.8,
    pnlPercentage: -1.74,
  },
]

const RECENT_SIGNALS = [
  {
    date: '18 May 2025',
    symbol: 'HDFCBANK',
    company: 'HDFC Bank Ltd.',
    signal: 'BUY',
    price: 1723.5,
    confidence: 82,
  },
  {
    date: '18 May 2025',
    symbol: 'TCS',
    company: 'Tata Consultancy Services',
    signal: 'BUY',
    price: 3645.2,
    confidence: 77,
  },
  {
    date: '18 May 2025',
    symbol: 'SBIN',
    company: 'State Bank of India',
    signal: 'HOLD',
    price: 812.35,
    confidence: 58,
  },
  {
    date: '18 May 2025',
    symbol: 'RELIANCE',
    company: 'Reliance Industries',
    signal: 'BUY',
    price: 2946.8,
    confidence: 75,
  },
  {
    date: '18 May 2025',
    symbol: 'INFY',
    company: 'Infosys Ltd.',
    signal: 'WATCH',
    price: 1512.4,
    confidence: 48,
  },
]

const RECENT_TRADES = [
  {
    date: '18 May 2025, 10:30 AM',
    symbol: 'HDFCBANK',
    type: 'BUY',
    quantity: 10,
    price: 1723.5,
    amount: 17235,
    status: 'Executed',
  },
  {
    date: '17 May 2025, 11:15 AM',
    symbol: 'TCS',
    type: 'BUY',
    quantity: 7,
    price: 3645.2,
    amount: 25516.4,
    status: 'Executed',
  },
  {
    date: '17 May 2025, 09:45 AM',
    symbol: 'RELIANCE',
    type: 'BUY',
    quantity: 5,
    price: 2946.8,
    amount: 14734,
    status: 'Executed',
  },
]

const ALLOCATION_DATA = [
  { symbol: 'HDFCBANK', percentage: 21.8 },
  { symbol: 'TCS', percentage: 32.6 },
  { symbol: 'RELIANCE', percentage: 18.7 },
  { symbol: 'INFY', percentage: 15.2 },
  { symbol: 'SBIN', percentage: 11.7 },
  { symbol: 'Cash', percentage: 4.7 },
]

const ALLOCATION_COLORS = [
  '#3b82f6',
  '#22c55e',
  '#f59e0b',
  '#a855f7',
  '#ef4444',
  '#06b6d4',
]

const PERFORMANCE_POINTS = {
  '1D': [0, 1, 0.5, 1.8, 1.4, 2.2, 2.7],
  '7D': [0, 1.8, 1.2, 3.2, 4.1, 3.7, 5.1],
  '1M': [0, 4, 7, 11, 9, 14, 12, 18, 16, 21, 19, 24.58],
  '3M': [0, 3, 7, 5, 12, 16, 13, 20, 18, 23, 21, 24.58],
  '1Y': [0, 5, 9, 13, 12, 18, 22, 20, 24, 28, 25, 24.58],
  All: [0, 4, 8, 12, 11, 17, 21, 19, 24, 28, 25, 24.58],
}

/* =========================================================
   FORMATTERS
   ========================================================= */

function formatCurrency(value) {
  return `₹${Number(value || 0).toLocaleString('en-IN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`
}

function formatPercentage(value) {
  return `${value >= 0 ? '+' : ''}${Number(value).toFixed(2)}%`
}

/* =========================================================
   SIGNAL BADGE
   ========================================================= */

function SignalBadge({ signal }) {
  return (
    <span className={`pt-signal pt-signal-${signal.toLowerCase()}`}>
      {signal}
    </span>
  )
}

/* =========================================================
   PERFORMANCE CHART
   ========================================================= */

function PerformanceChart({ selectedPeriod }) {
  const points =
    PERFORMANCE_POINTS[selectedPeriod] || PERFORMANCE_POINTS['1M']

  const width = 720
  const height = 280
  const paddingX = 28
  const paddingY = 24

  const min = Math.min(...points) - 3
  const max = Math.max(...points) + 3

  const chartPoints = points.map((value, index) => {
    const x =
      paddingX +
      (index / Math.max(points.length - 1, 1)) *
        (width - paddingX * 2)

    const y =
      height -
      paddingY -
      ((value - min) / (max - min)) *
        (height - paddingY * 2)

    return { x, y, value }
  })

  const linePoints = chartPoints
    .map((point) => `${point.x},${point.y}`)
    .join(' ')

  const areaPoints = [
    `${paddingX},${height - paddingY}`,
    linePoints,
    `${width - paddingX},${height - paddingY}`,
  ].join(' ')

  return (
    <svg
      className="pt-performance-svg"
      viewBox={`0 0 ${width} ${height}`}
      preserveAspectRatio="none"
      role="img"
      aria-label={`FinPilot paper trading performance for ${selectedPeriod}`}
    >
      {[0, 1, 2, 3, 4].map((line) => {
        const y =
          paddingY +
          (line / 4) * (height - paddingY * 2)

        return (
          <line
            key={line}
            x1={paddingX}
            y1={y}
            x2={width - paddingX}
            y2={y}
            stroke="rgba(105,145,180,0.16)"
            strokeWidth="1"
          />
        )
      })}

      <polygon
        points={areaPoints}
        fill="rgba(34,197,94,0.08)"
      />

      <polyline
        points={linePoints}
        fill="none"
        stroke="#22c55e"
        strokeWidth="3"
        strokeLinecap="round"
        strokeLinejoin="round"
      />

      {chartPoints.map((point, index) => (
        <circle
          key={`${point.value}-${index}`}
          cx={point.x}
          cy={point.y}
          r="3.5"
          fill="#22c55e"
          stroke="#081521"
          strokeWidth="2"
        />
      ))}

      <text
        x={width - 12}
        y="30"
        textAnchor="end"
        fill="#8eb4d9"
        fontSize="13"
      >
        FinPilot Paper
      </text>

      <text
        x={width - 12}
        y="49"
        textAnchor="end"
        fill="#22c55e"
        fontSize="14"
        fontWeight="700"
      >
        +24.58%
      </text>

      <text
        x={paddingX}
        y={height - 3}
        fill="#6688a9"
        fontSize="11"
      >
        18 Apr
      </text>

      <text
        x={width * 0.32}
        y={height - 3}
        textAnchor="middle"
        fill="#6688a9"
        fontSize="11"
      >
        25 Apr
      </text>

      <text
        x={width * 0.58}
        y={height - 3}
        textAnchor="middle"
        fill="#6688a9"
        fontSize="11"
      >
        2 May
      </text>

      <text
        x={width * 0.78}
        y={height - 3}
        textAnchor="middle"
        fill="#6688a9"
        fontSize="11"
      >
        9 May
      </text>

      <text
        x={width - paddingX}
        y={height - 3}
        textAnchor="end"
        fill="#6688a9"
        fontSize="11"
      >
        16 May
      </text>
    </svg>
  )
}

/* =========================================================
   PORTFOLIO ALLOCATION
   ========================================================= */

function AllocationChart() {
  const radius = 74
  const center = 100
  const circumference = 2 * Math.PI * radius

  const allocationTotal = ALLOCATION_DATA.reduce(
    (sum, item) => sum + item.percentage,
    0
  )

  let accumulated = 0

  return (
    <div className="pt-allocation-layout">
      <div className="pt-allocation-donut-wrap">
        <svg
          viewBox="0 0 200 200"
          className="pt-allocation-svg"
          role="img"
          aria-label="Portfolio allocation"
        >
          <circle
            cx={center}
            cy={center}
            r={radius}
            fill="none"
            stroke="#203a51"
            strokeWidth="24"
          />

          {ALLOCATION_DATA.map((item, index) => {
            const normalizedPercentage =
              (item.percentage / allocationTotal) * 100

            const dashLength =
              (normalizedPercentage / 100) *
              circumference

            const dashOffset =
              -(accumulated / 100) *
              circumference

            accumulated += normalizedPercentage

            return (
              <circle
                key={item.symbol}
                cx={center}
                cy={center}
                r={radius}
                fill="none"
                stroke={ALLOCATION_COLORS[index]}
                strokeWidth="24"
                strokeDasharray={`${dashLength} ${
                  circumference - dashLength
                }`}
                strokeDashoffset={dashOffset}
                strokeLinecap="butt"
                transform="rotate(-90 100 100)"
              />
            )
          })}
        </svg>

        <div className="pt-allocation-center">
          <span>Total</span>
          <strong>₹81,768.05</strong>
        </div>
      </div>

      <div className="pt-allocation-legend">
        {ALLOCATION_DATA.map((item, index) => (
          <div
            className="pt-allocation-item"
            key={item.symbol}
          >
            <span
              className="pt-allocation-dot"
              style={{
                backgroundColor: ALLOCATION_COLORS[index],
              }}
            />

            <span>{item.symbol}</span>

            <strong>{item.percentage}%</strong>
          </div>
        ))}
      </div>
    </div>
  )
}

/* =========================================================
   TRADE HISTORY
   ========================================================= */

function TradeHistoryChart() {
  const winningTrades = 19
  const losingTrades = 9
  const totalTrades = winningTrades + losingTrades

  const radius = 58
  const circumference = 2 * Math.PI * radius

  const winningLength =
    (winningTrades / totalTrades) * circumference

  const losingLength =
    (losingTrades / totalTrades) * circumference

  return (
    <div className="pt-history-content">
      <div className="pt-history-donut-wrap">
        <svg
          viewBox="0 0 160 160"
          className="pt-history-svg"
          role="img"
          aria-label="Trade history"
        >
          <circle
            cx="80"
            cy="80"
            r={radius}
            fill="none"
            stroke="#203a51"
            strokeWidth="20"
          />

          <circle
            cx="80"
            cy="80"
            r={radius}
            fill="none"
            stroke="#22c55e"
            strokeWidth="20"
            strokeDasharray={`${winningLength} ${
              circumference - winningLength
            }`}
            strokeDashoffset="0"
            transform="rotate(-90 80 80)"
          />

          <circle
            cx="80"
            cy="80"
            r={radius}
            fill="none"
            stroke="#ef4444"
            strokeWidth="20"
            strokeDasharray={`${losingLength} ${
              circumference - losingLength
            }`}
            strokeDashoffset={-winningLength}
            transform="rotate(-90 80 80)"
          />
        </svg>

        <div className="pt-history-center">
          <strong>{totalTrades}</strong>
          <span>Total Trades</span>
        </div>
      </div>

      <div className="pt-history-stats">
        <div>
          <span className="pt-history-dot winning-dot" />
          <span>Winning Trades</span>
          <strong>19 (67.86%)</strong>
        </div>

        <div>
          <span className="pt-history-dot losing-dot" />
          <span>Losing Trades</span>
          <strong>9 (32.14%)</strong>
        </div>

        <div>
          <span className="pt-history-dot win-rate-dot" />
          <span>Win Rate</span>
          <strong>67.86%</strong>
        </div>
      </div>
    </div>
  )
}

/* =========================================================
   MAIN COMPONENT
   ========================================================= */

function PaperTrading() {
  const [selectedPeriod, setSelectedPeriod] =
    useState('1M')

  const [positions] =
    useState(INITIAL_POSITIONS)

  const [signals] =
    useState(RECENT_SIGNALS)

  const [trades] =
    useState(RECENT_TRADES)

  const [marketMode, setMarketMode] =
    useState('Live Market')

  const totalInvested = useMemo(
    () =>
      positions.reduce(
        (total, position) =>
          total +
          position.quantity *
            position.averagePrice,
        0
      ),
    [positions]
  )

  const totalPortfolioValue = useMemo(
    () =>
      positions.reduce(
        (total, position) =>
          total +
          position.quantity *
            position.currentPrice,
        0
      ),
    [positions]
  )

  const totalPnL =
    totalPortfolioValue - totalInvested

  return (
    <div className="page paper-trading-page pt-page">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <header className="pt-header">
        <div>
          <h2>Paper Trading</h2>

          <p>
            Trade with virtual money. Track performance
            of AI-powered recommendations.
          </p>
        </div>

        <div className="pt-market-selector">
          <span className="pt-status-dot" />

          <select
            value={marketMode}
            onChange={(event) =>
              setMarketMode(event.target.value)
            }
            aria-label="Market mode"
          >
            <option>Live Market</option>
            <option>Market Simulation</option>
          </select>
        </div>
      </header>

      {/* =====================================================
          SUMMARY CARDS
      ===================================================== */}

      <section className="pt-stats-grid">

        <div className="pt-stat-card">
          <div className="pt-stat-top">
            <span>Virtual Balance</span>
            <div className="pt-stat-icon">▣</div>
          </div>

          <strong>₹1,00,000.00</strong>

          <small>
            Available to invest
          </small>
        </div>

        <div className="pt-stat-card">
          <div className="pt-stat-top">
            <span>Total Portfolio Value</span>
            <div className="pt-stat-icon">▣</div>
          </div>

          <strong>
            {formatCurrency(totalPortfolioValue)}
          </strong>

          <small>
            Invested:{' '}
            <b>
              {formatCurrency(totalInvested)}
            </b>
          </small>

          <div className="pt-stat-pnl">
            P&amp;L: +₹2,435.25 (+3.07%)
          </div>
        </div>

        <div className="pt-stat-card">
          <div className="pt-stat-top">
            <span>Today's P&amp;L</span>
          </div>

          <strong className="pt-positive">
            +₹1,250.75
          </strong>

          <small className="pt-positive">
            +1.02%
          </small>

          <div
            className="pt-mini-line"
            aria-hidden="true"
          >
            {Array.from({ length: 9 }).map(
              (_, index) => (
                <span key={index} />
              )
            )}
          </div>
        </div>

        <div className="pt-stat-card">
          <div className="pt-stat-top">
            <span>Total Return</span>
          </div>

          <strong className="pt-positive">
            +24.58%
          </strong>

          <small>
            All time
          </small>

          <div
            className="pt-mini-bars"
            aria-hidden="true"
          >
            {Array.from({ length: 6 }).map(
              (_, index) => (
                <span key={index} />
              )
            )}
          </div>
        </div>

      </section>

      {/* =====================================================
          AI SIGNALS + ALLOCATION
      ===================================================== */}

      <section className="pt-two-column">

        <div className="pt-card">

          <div className="pt-card-header">
            <h3>AI Recent Signals</h3>

            <button
              type="button"
              className="pt-view-button"
            >
              View all
            </button>
          </div>

          <div className="pt-table-scroll">

            <table className="pt-table">

              <thead>
                <tr>
                  <th>Date</th>
                  <th>Stock</th>
                  <th>Signal</th>
                  <th>Price</th>
                  <th>Confidence</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {signals.map((signal) => (
                  <tr key={signal.symbol}>

                    <td>
                      {signal.date}
                    </td>

                    <td>
                      <div className="pt-stock-cell">
                        <strong>
                          {signal.symbol}
                        </strong>

                        <small>
                          {signal.company}
                        </small>
                      </div>
                    </td>

                    <td>
                      <SignalBadge
                        signal={signal.signal}
                      />
                    </td>

                    <td>
                      {formatCurrency(signal.price)}
                    </td>

                    <td>
                      <div className="pt-confidence">

                        <span className="pt-confidence-value">
                          {signal.confidence}/100
                        </span>

                        <div className="pt-confidence-bar">
                          <span
                            style={{
                              width: `${signal.confidence}%`,
                            }}
                          />
                        </div>

                      </div>
                    </td>

                    <td>
                      <button
                        type="button"
                        className="pt-trade-button"
                        onClick={() =>
                          console.log(
                            `Trade ${signal.symbol}`
                          )
                        }
                      >
                        Trade
                      </button>
                    </td>

                  </tr>
                ))}
              </tbody>

            </table>

          </div>
        </div>

        <div className="pt-card pt-allocation-card">

          <div className="pt-card-header">
            <h3>Portfolio Allocation</h3>
          </div>

          <AllocationChart />

          <p className="pt-allocation-footer">
            Holdings spread across 5 stocks
          </p>

        </div>

      </section>

      {/* =====================================================
          OPEN POSITIONS + PERFORMANCE
      ===================================================== */}

      <section className="pt-two-column">

        <div className="pt-card pt-positions-card">

          <div className="pt-card-header">

            <h3>Open Positions</h3>

            <button
              type="button"
              className="pt-view-button"
            >
              View all positions →
            </button>

          </div>

          <div className="pt-table-scroll">

            <table className="pt-table pt-positions-table">

              <thead>
                <tr>
                  <th>Stock</th>
                  <th>Quantity</th>
                  <th>Avg. Price</th>
                  <th>Current Price</th>
                  <th>P&amp;L</th>
                  <th>P&amp;L %</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>

                {positions.map((position) => (
                  <tr key={position.symbol}>

                    <td>
                      <strong>
                        {position.symbol}
                      </strong>
                    </td>

                    <td>
                      {position.quantity}
                    </td>

                    <td>
                      {formatCurrency(
                        position.averagePrice
                      )}
                    </td>

                    <td>
                      {formatCurrency(
                        position.currentPrice
                      )}
                    </td>

                    <td
                      className={
                        position.pnl >= 0
                          ? 'pt-positive'
                          : 'pt-negative'
                      }
                    >
                      {position.pnl >= 0
                        ? '+'
                        : ''}
                      {formatCurrency(
                        position.pnl
                      )}
                    </td>

                    <td
                      className={
                        position.pnlPercentage >= 0
                          ? 'pt-positive'
                          : 'pt-negative'
                      }
                    >
                      {formatPercentage(
                        position.pnlPercentage
                      )}
                    </td>

                    <td>
                      <button
                        type="button"
                        className="pt-exit-button"
                        onClick={() =>
                          console.log(
                            `Exit ${position.symbol}`
                          )
                        }
                      >
                        Exit
                      </button>
                    </td>

                  </tr>
                ))}

              </tbody>

            </table>

          </div>

          <div className="pt-table-footer">
            Showing 1 to {positions.length} of{' '}
            {positions.length} positions
          </div>

        </div>

        <div className="pt-card pt-performance-card">

          <div className="pt-card-header">
            <h3>Performance Chart</h3>
          </div>

          <div className="pt-chart-controls">

            <div className="pt-period-buttons">

              {[
                '1D',
                '7D',
                '1M',
                '3M',
                '1Y',
                'All',
              ].map((period) => (
                <button
                  type="button"
                  key={period}
                  className={
                    selectedPeriod === period
                      ? 'active'
                      : ''
                  }
                  onClick={() =>
                    setSelectedPeriod(period)
                  }
                >
                  {period}
                </button>
              ))}

            </div>

            <div className="pt-chart-compare">

              <span>
                Compare to
              </span>

              <select
                defaultValue="NIFTY 50"
                aria-label="Compare performance"
              >
                <option>NIFTY 50</option>
                <option>SENSEX</option>
                <option>Bank NIFTY</option>
              </select>

            </div>

          </div>

          <div className="pt-performance-chart">
            <PerformanceChart
              selectedPeriod={selectedPeriod}
            />
          </div>

          <div className="pt-chart-legend">

            <span>
              <i className="pt-legend-line" />

              FinPilot Paper{' '}
              <strong>
                +24.58%
              </strong>
            </span>

            <span>
              <i className="pt-legend-line pt-legend-nifty" />

              NIFTY 50{' '}
              <strong>
                +6.21%
              </strong>
            </span>

          </div>

        </div>

      </section>

      {/* =====================================================
          RECENT TRADES + TRADE HISTORY
      ===================================================== */}

      <section className="pt-two-column pt-bottom-section">

        <div className="pt-card pt-recent-trades-card">

          <div className="pt-card-header">
            <h3>Recent Trades</h3>
          </div>

          <div className="pt-table-scroll">

            <table className="pt-table">

              <thead>
                <tr>
                  <th>Date</th>
                  <th>Stock</th>
                  <th>Type</th>
                  <th>Quantity</th>
                  <th>Price</th>
                  <th>Amount</th>
                  <th>Status</th>
                </tr>
              </thead>

              <tbody>

                {trades.map((trade, index) => (
                  <tr
                    key={`${trade.symbol}-${index}`}
                  >

                    <td>
                      {trade.date}
                    </td>

                    <td>
                      <strong>
                        {trade.symbol}
                      </strong>
                    </td>

                    <td>
                      <SignalBadge
                        signal={trade.type}
                      />
                    </td>

                    <td>
                      {trade.quantity}
                    </td>

                    <td>
                      {formatCurrency(
                        trade.price
                      )}
                    </td>

                    <td>
                      {formatCurrency(
                        trade.amount
                      )}
                    </td>

                    <td className="pt-trade-status">
                      {trade.status}
                    </td>

                  </tr>
                ))}

              </tbody>

            </table>

          </div>

        </div>

        <div className="pt-card pt-history-card">

          <div className="pt-card-header">
            <h3>Trade History</h3>
          </div>

          <TradeHistoryChart />

        </div>

      </section>

      {/* =====================================================
          FOOTER NOTE
      ===================================================== */}

      <div className="pt-note">

        <span>
          Paper trading uses virtual money and does not
          involve real financial transactions.
        </span>

        <span>
          Portfolio P&amp;L:{' '}

          <strong
            className={
              totalPnL >= 0
                ? 'pt-positive'
                : 'pt-negative'
            }
          >
            {formatCurrency(totalPnL)}
          </strong>
        </span>

      </div>

    </div>
  )
}

export default PaperTrading