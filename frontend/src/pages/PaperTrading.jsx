import {
  useEffect,
  useMemo,
  useState,
} from 'react'

import {
  useLocation,
} from 'react-router-dom'

import {
  buyStock,
  sellStock,
  getPaperAccount,
  getPaperPositions,
  getPaperPortfolio,
  getPaperTrades,
  getMarketStatus,
} from '../services/api'

import { getToken } from '../services/auth'

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
    <span
      className={`pt-signal pt-signal-${signal.toLowerCase()}`}
    >
      {signal}
    </span>
  )
}

/* =========================================================
   PERFORMANCE CHART
   ========================================================= */

function PerformanceChart({ selectedPeriod }) {
  const points =
    PERFORMANCE_POINTS[selectedPeriod] ||
    PERFORMANCE_POINTS['1M']

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

function AllocationChart({
  allocation,
  totalValue,
}) {
  const radius = 74
  const center = 100
  const circumference = 2 * Math.PI * radius

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

          {allocation.map((item, index) => {
            const normalizedPercentage =
              Number(item.percentage || 0)

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
                stroke={
                  ALLOCATION_COLORS[
                    index % ALLOCATION_COLORS.length
                  ]
                }
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

          <strong>
            {formatCurrency(totalValue)}
          </strong>
        </div>
      </div>

      <div className="pt-allocation-legend">
        {allocation.map((item, index) => (
          <div
            className="pt-allocation-item"
            key={item.symbol}
          >
            <span
              className="pt-allocation-dot"
              style={{
                backgroundColor:
                  ALLOCATION_COLORS[
                    index % ALLOCATION_COLORS.length
                  ],
              }}
            />

            <span>{item.symbol}</span>

            <strong>
              {Number(item.percentage || 0).toFixed(2)}%
            </strong>
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
  const totalTrades =
    winningTrades + losingTrades

  const radius = 58
  const circumference = 2 * Math.PI * radius

  const winningLength =
    (winningTrades / totalTrades) *
    circumference

  const losingLength =
    (losingTrades / totalTrades) *
    circumference

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

  const location = useLocation()

  const [selectedPeriod, setSelectedPeriod] =
    useState('1M')

  const [positions, setPositions] =
    useState(INITIAL_POSITIONS)

  const [signals] =
    useState(RECENT_SIGNALS)

  const [trades, setTrades] =
    useState(RECENT_TRADES)

  const [cashBalance, setCashBalance] =
    useState(100000)

  const [portfolio, setPortfolio] =
    useState(null)

  const [isRefreshing, setIsRefreshing] =
    useState(false)

  const [lastUpdated, setLastUpdated] =
    useState(null)

  const [marketStatus, setMarketStatus] =
    useState(null)

  /* =======================================================
     ORDER STATE
     ======================================================= */

  const [order, setOrder] =
    useState(null)

  const [orderSide, setOrderSide] =
    useState('BUY')

  const [quantity, setQuantity] =
    useState('')

  const [orderError, setOrderError] =
    useState('')

  const [orderSuccess, setOrderSuccess] =
    useState('')

  const [isSubmitting, setIsSubmitting] =
    useState(false)

  /* =======================================================
     LOAD PAPER TRADING DATA
     ======================================================= */

  const loadPaperTradingData = async () => {
    const token = getToken()

    if (!token) {
      return
    }

    try {
      const [
        accountData,
        positionsData,
        portfolioData,
        tradesData,
        marketStatusData,
      ] = await Promise.all([
        getPaperAccount(token),
        getPaperPositions(token),
        getPaperPortfolio(token),
        getPaperTrades(token),
        getMarketStatus(token),
      ])

      setCashBalance(
        Number(accountData.cash_balance ?? 0)
      )

      setPortfolio(portfolioData)

      setMarketStatus(marketStatusData)

      setLastUpdated(
        marketStatusData?.last_updated ||
          new Date().toISOString()
      )

      setPositions(
        Array.isArray(positionsData)
          ? positionsData.map((position) => ({
              symbol: position.symbol,
              quantity: Number(
                position.quantity ?? 0
              ),
              averagePrice: Number(
                position.average_price ??
                  position.averagePrice ??
                  0
              ),
              currentPrice: Number(
                position.current_price ??
                  position.currentPrice ??
                  0
              ),
              pnl: Number(
                position.pnl ??
                  position.profit_loss ??
                  0
              ),
              pnlPercentage: Number(
                position.pnl_percentage ??
                  position.pnlPercentage ??
                  0
              ),
            }))
          : []
      )

      setTrades(
        Array.isArray(tradesData)
          ? tradesData.map((trade) => ({
              date: trade.created_at
                ? new Date(
                    trade.created_at
                  ).toLocaleString('en-IN')
                : 'N/A',
              symbol: trade.symbol,
              type: trade.side,
              quantity: Number(
                trade.quantity ?? 0
              ),
              price: Number(
                trade.price ?? 0
              ),
              amount: Number(
                trade.total_value ??
                  trade.amount ??
                  0
              ),
              status: 'Executed',
            }))
          : []
      )
    } catch (error) {
      console.error(
        'Failed to load paper trading data:',
        error
      )
    }
  }

  const handleRefresh = async () => {
    setIsRefreshing(true)

    try {
      await loadPaperTradingData()
    } finally {
      setIsRefreshing(false)
    }
  }

  useEffect(() => {
    loadPaperTradingData()
  }, [])

  /* =======================================================
     OPEN BUY ORDER
     ======================================================= */

  const openBuyOrder = (stock) => {
    setOrder({
      symbol: stock.symbol,
      price: Number(stock.price || 0),
    })

    setOrderSide('BUY')
    setQuantity('')
    setOrderError('')
    setOrderSuccess('')
  }

  useEffect(() => {
    const quickTrade =
      location.state?.quickTrade

    if (!quickTrade) {
      return
    }

    openBuyOrder({
      symbol: quickTrade.symbol,
      price: quickTrade.price,
    })
  }, [location.state])
    
  /* =======================================================
     OPEN SELL ORDER
     ======================================================= */

  const openSellOrder = (position) => {
    setOrder({
      symbol: position.symbol,
      price: Number(
        position.currentPrice || 0
      ),
      maxQuantity: Number(
        position.quantity || 0
      ),
    })

    setOrderSide('SELL')
    setQuantity('')
    setOrderError('')
    setOrderSuccess('')
  }

  /* =======================================================
     ORDER VALUE
     ======================================================= */

  const orderValue = useMemo(() => {
    if (!order) {
      return 0
    }

    const parsedQuantity = Number(quantity)

    if (!Number.isFinite(parsedQuantity)) {
      return 0
    }

    return (
      parsedQuantity *
      Number(order.price || 0)
    )
  }, [order, quantity])

  /* =======================================================
     SUBMIT ORDER
     ======================================================= */

  const handleOrderSubmit = async () => {
    setOrderError('')
    setOrderSuccess('')

    const parsedQuantity = Number(quantity)
    const parsedPrice = Number(
      order?.price || 0
    )

    if (!order) {
      return
    }

    if (
      !Number.isInteger(parsedQuantity) ||
      parsedQuantity <= 0
    ) {
      setOrderError(
        'Quantity must be a positive whole number.'
      )
      return
    }

    if (
      !Number.isFinite(parsedPrice) ||
      parsedPrice <= 0
    ) {
      setOrderError(
        'Current price is unavailable.'
      )
      return
    }

    if (
      orderSide === 'SELL' &&
      parsedQuantity >
        Number(order.maxQuantity || 0)
    ) {
      setOrderError(
        `You can sell a maximum of ${order.maxQuantity} shares.`
      )
      return
    }

    const calculatedOrderValue =
      parsedQuantity * parsedPrice

    if (
      orderSide === 'BUY' &&
      calculatedOrderValue > cashBalance
    ) {
      setOrderError(
        'Insufficient virtual balance for this order.'
      )
      return
    }

    const token = getToken()

    if (!token) {
      setOrderError(
        'Your session has expired. Please log in again.'
      )
      return
    }

    setIsSubmitting(true)

    try {
      if (orderSide === 'BUY') {
        await buyStock(
          order.symbol,
          parsedQuantity,
          token
        )

        setOrderSuccess(
          `${order.symbol} BUY order executed successfully.`
        )
      } else {
        await sellStock(
          order.symbol,
          parsedQuantity,
          token
        )

        setOrderSuccess(
          `${order.symbol} SELL order executed successfully.`
        )
      }

      await loadPaperTradingData()

      setQuantity('')
    } catch (error) {
      setOrderError(
        error.message ||
          'Unable to execute the order.'
      )
    } finally {
      setIsSubmitting(false)
    }
  }

  /* =======================================================
     CLOSE ORDER MODAL
     ======================================================= */

  const closeOrderModal = () => {
    if (isSubmitting) {
      return
    }

    setOrder(null)
    setQuantity('')
    setOrderError('')
    setOrderSuccess('')
  }

  /* =======================================================
     PORTFOLIO CALCULATIONS
     ======================================================= */

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

  /* =======================================================
     REAL PORTFOLIO ALLOCATION
     ======================================================= */

  const portfolioAllocation =
    Array.isArray(portfolio?.allocation)
      ? portfolio.allocation
      : []

  const portfolioTotalValue =
    Number(portfolio?.cash_balance || 0) +
    Number(portfolio?.current_value || 0)

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

          {lastUpdated && (
            <small>
              Last updated:{' '}
              {new Date(lastUpdated).toLocaleTimeString(
                'en-IN'
              )}
            </small>
          )}
        </div>

        <div className="pt-market-selector">
          <span
            className="pt-status-dot"
            style={{
              backgroundColor:
                marketStatus?.status === 'OPEN'
                  ? '#22c55e'
                  : '#ef4444',
            }}
          />

          <span>
            {marketStatus?.status === 'OPEN'
              ? 'Market Open'
              : 'Market Closed'}
          </span>

          <button
            type="button"
            className="pt-view-button"
            onClick={handleRefresh}
            disabled={isRefreshing}
          >
            {isRefreshing ? 'Refreshing...' : '↻ Refresh'}
          </button>
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

          <strong>
            {formatCurrency(cashBalance)}
          </strong>

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
            {formatCurrency(
              totalPortfolioValue
            )}
          </strong>

          <small>
            Invested:{' '}
            <b>
              {formatCurrency(totalInvested)}
            </b>
          </small>

          <div className="pt-stat-pnl">
            P&amp;L:{' '}
            {totalPnL >= 0 ? '+' : ''}
            {formatCurrency(totalPnL)}
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
                      {formatCurrency(
                        signal.price
                      )}
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
                          openBuyOrder(signal)
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

          <AllocationChart
            allocation={portfolioAllocation}
            totalValue={portfolioTotalValue}
          />

          <p className="pt-allocation-footer">
            Holdings spread across{' '}
            {positions.length} stocks
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
                          openSellOrder(position)
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

      {/* =====================================================
          ORDER MODAL
      ===================================================== */}

      {order && (
        <div className="pt-order-overlay">

          <div
            className="pt-order-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="order-modal-title"
          >

            {/* ORDER HEADER */}

            <div className="pt-order-header">

              <div>
                <span className="pt-order-label">
                  Paper Trading
                </span>

                <h3 id="order-modal-title">
                  Place Order
                </h3>
              </div>

              <button
                type="button"
                className="pt-order-close"
                onClick={closeOrderModal}
                disabled={isSubmitting}
                aria-label="Close order modal"
              >
                ×
              </button>

            </div>

            {/* STOCK INFORMATION */}

            <div className="pt-order-stock">

              <strong>
                {order.symbol}
              </strong>

              <span>
                Current Price:{' '}
                {formatCurrency(order.price)}
              </span>

            </div>

            {/* BUY / SELL */}

            <div className="pt-order-side">

              <button
                type="button"
                className={
                  orderSide === 'BUY'
                    ? 'active'
                    : ''
                }
                onClick={() => {
                  setOrderSide('BUY')
                  setOrderError('')
                  setOrderSuccess('')
                }}
                disabled={isSubmitting}
              >
                BUY
              </button>

              <button
                type="button"
                className={
                  orderSide === 'SELL'
                    ? 'active sell-active'
                    : ''
                }
                onClick={() => {
                  setOrderSide('SELL')
                  setOrderError('')
                  setOrderSuccess('')
                }}
                disabled={isSubmitting}
              >
                SELL
              </button>

            </div>

            {/* QUANTITY */}

            <div className="pt-order-field">

              <label htmlFor="order-quantity">
                Quantity
              </label>

              <input
                id="order-quantity"
                type="number"
                min="1"
                step="1"
                value={quantity}
                onChange={(event) =>
                  setQuantity(
                    event.target.value
                  )
                }
                placeholder="Enter quantity"
                disabled={isSubmitting}
              />

              {orderSide === 'SELL' && (
                <small>
                  Available quantity:{' '}
                  {order.maxQuantity}
                </small>
              )}

            </div>

            {/* PRICE */}

            <div className="pt-order-field">

              <label htmlFor="order-price">
                Price
              </label>

              <input
                id="order-price"
                type="number"
                value={order.price}
                readOnly
              />

              <small>
                Execution price is determined by
                the backend using current market data.
              </small>

            </div>

            {/* ORDER VALUE */}

            <div className="pt-order-summary">

              <span>
                Order Value
              </span>

              <strong>
                {formatCurrency(orderValue)}
              </strong>

            </div>

            {/* AVAILABLE BALANCE */}

            {orderSide === 'BUY' && (
              <div className="pt-order-balance">

                Available Balance:{' '}

                <strong>
                  {formatCurrency(cashBalance)}
                </strong>

              </div>
            )}

            {/* ERROR */}

            {orderError && (
              <div className="pt-order-error">
                {orderError}
              </div>
            )}

            {/* SUCCESS */}

            {orderSuccess && (
              <div className="pt-order-success">
                {orderSuccess}
              </div>
            )}

            {/* ACTION BUTTONS */}

            <div className="pt-order-actions">

              <button
                type="button"
                className="pt-order-cancel"
                onClick={closeOrderModal}
                disabled={isSubmitting}
              >
                Cancel
              </button>

              <button
                type="button"
                className={
                  orderSide === 'BUY'
                    ? 'pt-order-confirm buy'
                    : 'pt-order-confirm sell'
                }
                onClick={handleOrderSubmit}
                disabled={isSubmitting}
              >
                {isSubmitting
                  ? 'Processing...'
                  : `Confirm ${orderSide}`}
              </button>

            </div>

          </div>

        </div>
      )}

    </div>
  )
}

export default PaperTrading