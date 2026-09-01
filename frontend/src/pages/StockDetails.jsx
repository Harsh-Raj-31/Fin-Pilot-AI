import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

const API_BASE_URL =
  'http://127.0.0.1:8000/api/v1'

function StockDetails() {
  const { symbol } = useParams()
  const navigate = useNavigate()

  const [stock, setStock] = useState(null)
  const [performance, setPerformance] = useState(null)
  const [risk, setRisk] = useState(null)
  const [score, setScore] = useState(null)
  const [signal, setSignal] = useState(null)
  const [indicators, setIndicators] = useState(null)
  const [explanation, setExplanation] = useState(null)

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let cancelled = false

    async function fetchStockDetails() {
      try {
        setLoading(true)
        setError('')

        const token = localStorage.getItem(
          'finpilot_access_token'
        )

        const headers = token
          ? {
              Authorization: `Bearer ${token}`,
            }
          : {}

        const endpoints = [
          ['stock', `/stocks/${symbol}`],
          ['performance', `/stocks/${symbol}/performance`],
          ['risk', `/stocks/${symbol}/risk`],
          ['score', `/stocks/${symbol}/score`],
          ['signal', `/stocks/${symbol}/signal`],
          ['indicators', `/stocks/${symbol}/indicators`],
          [
            'explanation',
            `/stocks/${symbol}/explanation`,
          ],
        ]

        const results = await Promise.all(
          endpoints.map(async ([name, endpoint]) => {
            const response = await fetch(
              `${API_BASE_URL}${endpoint}`,
              {
                headers,
              }
            )

            const data = await response.json()

            if (!response.ok) {
              throw new Error(
                data?.detail ||
                  `Unable to load ${name}.`
              )
            }

            return [name, data]
          })
        )

        if (cancelled) {
          return
        }

        const data = Object.fromEntries(results)

        setStock(data.stock)
        setPerformance(data.performance)
        setRisk(data.risk)
        setScore(data.score)
        setSignal(data.signal)
        setIndicators(data.indicators)
        setExplanation(data.explanation)
      } catch (err) {
        console.error(
          'Stock details error:',
          err
        )

        if (!cancelled) {
          setError(
            err.message ||
              'Unable to load stock details.'
          )
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    if (symbol) {
      fetchStockDetails()
    }

    return () => {
      cancelled = true
    }
  }, [symbol])

  function formatCurrency(value) {
    if (
      value === null ||
      value === undefined
    ) {
      return '—'
    }

    return `₹${Number(value).toLocaleString(
      'en-IN',
      {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      }
    )}`
  }

  function formatPercentage(value) {
    if (
      value === null ||
      value === undefined
    ) {
      return '—'
    }

    return `${Number(value).toFixed(2)}%`
  }

  function formatNumber(value) {
    if (
      value === null ||
      value === undefined
    ) {
      return '—'
    }

    return Number(value).toLocaleString(
      'en-IN',
      {
        maximumFractionDigits: 2,
      }
    )
  }

  function getValueClass(value) {
    if (
      value === null ||
      value === undefined
    ) {
      return ''
    }

    return Number(value) >= 0
      ? 'positive'
      : 'negative'
  }

  function getRiskClass(level) {
    const value = String(
      level || ''
    ).toLowerCase()

    if (value === 'high') {
      return 'negative'
    }

    if (value === 'low') {
      return 'positive'
    }

    return ''
  }

  function getSignalClass(value) {
    const signalValue = String(
      value || ''
    ).toLowerCase()

    if (
      signalValue.includes('buy')
    ) {
      return 'positive'
    }

    if (
      signalValue.includes('sell')
    ) {
      return 'negative'
    }

    return ''
  }

  if (loading) {
    return (
      <div className="page stock-details-page">
        <button
          type="button"
          className="back-button"
          onClick={() => navigate('/market')}
        >
          ← Back to Market
        </button>

        <div className="market-loading">
          Loading {symbol} analysis...
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="page stock-details-page">
        <button
          type="button"
          className="back-button"
          onClick={() => navigate('/market')}
        >
          ← Back to Market
        </button>

        <div className="market-error">
          <strong>
            Unable to load stock
          </strong>

          <span>{error}</span>
        </div>
      </div>
    )
  }

  return (
    <div className="page stock-details-page">

      {/* HEADER */}

      <div className="stock-details-header">

        <div>

          <button
            type="button"
            className="back-button"
            onClick={() => navigate('/market')}
          >
            ← Back to Market
          </button>

          <div className="stock-title">

            <div>
              <h2>
                {stock?.symbol ||
                  symbol}
              </h2>

              <p>
                {stock?.company_name ||
                  'Stock Analysis'}
              </p>
            </div>

            <div className="stock-meta">

              <span>
                {stock?.exchange ||
                  'N/A'}
              </span>

              <span>
                {stock?.sector ||
                  'N/A'}
              </span>

            </div>

          </div>

        </div>

        <div className="stock-price">

          <span>
            Current Price
          </span>

          <strong>
            {formatCurrency(
              stock?.current_price
            )}
          </strong>

        </div>

      </div>


      {/* SUMMARY CARDS */}

      <section className="stats-grid">

        <div className="stat-card">

          <span>
            Performance
          </span>

          <strong
            className={getValueClass(
              performance?.return_percentage
            )}
          >
            {formatPercentage(
              performance?.return_percentage
            )}
          </strong>

          <small>
            1-month return
          </small>

        </div>


        <div className="stat-card">

          <span>
            Risk
          </span>

          <strong
            className={getRiskClass(
              risk?.risk_level
            )}
          >
            {risk?.risk_level ||
              'N/A'}
          </strong>

          <small>
            Score:{' '}
            {formatNumber(
              risk?.risk_score
            )}
          </small>

        </div>


        <div className="stat-card">

          <span>
            AI Score
          </span>

          <strong>
            {score?.score ??
              score?.total_score ??
              'N/A'}
            {score &&
            (score?.score !== undefined ||
              score?.total_score !== undefined)
              ? '/100'
              : ''}
          </strong>

          <small>
            FinPilot scoring model
          </small>

        </div>


        <div className="stat-card">

          <span>
            AI Signal
          </span>

          <strong
            className={getSignalClass(
              signal?.signal
            )}
          >
            {signal?.signal ||
              'N/A'}
          </strong>

          <small>
            Current model signal
          </small>

        </div>

      </section>


      {/* MAIN GRID */}

      <section className="dashboard-grid stock-analysis-grid">

        {/* PERFORMANCE */}

        <div className="dashboard-card">

          <div className="card-heading">
            <div>
              <h3>
                Performance
              </h3>

              <p>
                Recent stock performance.
              </p>
            </div>
          </div>

          <div className="detail-list">

            <div>
              <span>
                Return
              </span>

              <strong
                className={getValueClass(
                  performance?.return_percentage
                )}
              >
                {formatPercentage(
                  performance?.return_percentage
                )}
              </strong>
            </div>

            <div>
              <span>
                Current Price
              </span>

              <strong>
                {formatCurrency(
                  stock?.current_price
                )}
              </strong>
            </div>

            <div>
              <span>
                Previous Close
              </span>

              <strong>
                {formatCurrency(
                  stock?.previous_close
                )}
              </strong>
            </div>

          </div>

        </div>


        {/* RISK */}

        <div className="dashboard-card">

          <div className="card-heading">
            <div>
              <h3>
                Risk Analysis
              </h3>

              <p>
                FinPilot risk assessment.
              </p>
            </div>
          </div>

          <div className="detail-list">

            <div>
              <span>
                Risk Level
              </span>

              <strong
                className={getRiskClass(
                  risk?.risk_level
                )}
              >
                {risk?.risk_level ||
                  'N/A'}
              </strong>
            </div>

            <div>
              <span>
                Risk Score
              </span>

              <strong>
                {formatNumber(
                  risk?.risk_score
                )}
              </strong>
            </div>

            <div>
              <span>
                Volatility
              </span>

              <strong>
                {formatNumber(
                  risk?.volatility
                )}
              </strong>
            </div>

            <div>
              <span>
                Maximum Drawdown
              </span>

              <strong className="negative">
                {formatPercentage(
                  risk?.maximum_drawdown
                )}
              </strong>
            </div>

          </div>

        </div>


        {/* INDICATORS */}

        <div className="dashboard-card">

          <div className="card-heading">
            <div>
              <h3>
                Technical Indicators
              </h3>

              <p>
                Current technical signals.
              </p>
            </div>
          </div>

          <div className="detail-list">

            <div>
              <span>
                RSI
              </span>

              <strong>
                {formatNumber(
                  indicators?.rsi
                )}
              </strong>
            </div>

            <div>
              <span>
                SMA 20
              </span>

              <strong>
                {formatCurrency(
                  indicators?.sma_20
                )}
              </strong>
            </div>

            <div>
              <span>
                EMA 20
              </span>

              <strong>
                {formatCurrency(
                  indicators?.ema_20
                )}
              </strong>
            </div>

            <div>
              <span>
                MACD
              </span>

              <strong>
                {formatNumber(
                  indicators?.macd
                )}
              </strong>
            </div>

            <div>
              <span>
                MACD Signal
              </span>

              <strong>
                {formatNumber(
                  indicators?.macd_signal
                )}
              </strong>
            </div>

          </div>

        </div>


        {/* AI SIGNAL */}

        <div className="dashboard-card">

          <div className="card-heading">
            <div>
              <h3>
                FinPilot AI Signal
              </h3>

              <p>
                Current model recommendation.
              </p>
            </div>
          </div>

          <div className="ai-signal-box">

            <strong
              className={getSignalClass(
                signal?.signal
              )}
            >
              {signal?.signal ||
                'N/A'}
            </strong>

            <span>
              Score:{' '}
              {score?.score ??
                score?.total_score ??
                'N/A'}
              /100
            </span>

          </div>

          <div className="explanation-box">

            <span>
              Why?
            </span>

            <p>
              {explanation?.explanation ||
                explanation?.message ||
                explanation?.response ||
                'No explanation available.'}
            </p>

          </div>

        </div>

      </section>

    </div>
  )
}

export default StockDetails