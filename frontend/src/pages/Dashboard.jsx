import { useEffect, useState } from 'react'

const API_BASE_URL =
  'http://127.0.0.1:8000/api/v1'


function Dashboard() {
  const [analytics, setAnalytics] =
    useState(null)

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState('')


  /* =====================================================
     FETCH PORTFOLIO ANALYTICS
  ===================================================== */

  useEffect(() => {
    let cancelled = false

    async function fetchAnalytics() {
      try {
        const token =
          localStorage.getItem(
            'finpilot_access_token'
          )

        if (!token) {
          throw new Error(
            'Authentication token not found.'
          )
        }

        const response = await fetch(
          `${API_BASE_URL}/portfolio/analytics`,
          {
            method: 'GET',
            headers: {
              Authorization:
                `Bearer ${token}`,
            },
          }
        )

        const data =
          await response.json()

        if (!response.ok) {
          throw new Error(
            data?.detail ||
              'Unable to load portfolio analytics.'
          )
        }

        if (!cancelled) {
          setAnalytics(data)
        }
      } catch (err) {
        console.error(
          'Portfolio analytics error:',
          err
        )

        if (!cancelled) {
          setError(
            err.message ||
              'Unable to load portfolio analytics.'
          )
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    fetchAnalytics()

    return () => {
      cancelled = true
    }
  }, [])


  /* =====================================================
     FORMATTERS
  ===================================================== */

  function formatCurrency(value) {
    return `₹${Number(
      value || 0
    ).toLocaleString('en-IN', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })}`
  }


  function formatPercentage(value) {
    return `${Number(
      value || 0
    ).toFixed(2)}%`
  }


  function getValueClass(value) {
    return Number(value || 0) >= 0
      ? 'positive'
      : 'negative'
  }


  function getRiskClass(level) {
    const normalized =
      String(level || '')
        .toLowerCase()

    if (normalized === 'high') {
      return 'risk-high'
    }

    if (normalized === 'low') {
      return 'risk-low'
    }

    return 'risk-medium'
  }


  /* =====================================================
     LOADING
  ===================================================== */

  if (loading) {
    return (
      <div className="page">

        <div className="page-header">
          <div>
            <h2>Dashboard</h2>

            <p>
              Loading your financial
              command center...
            </p>
          </div>
        </div>

        <section className="stats-grid">

          {[1, 2, 3, 4].map(
            (item) => (
              <div
                className="stat-card dashboard-skeleton"
                key={item}
              >
                <span></span>
                <strong></strong>
                <small></small>
              </div>
            )
          )}

        </section>

      </div>
    )
  }


  /* =====================================================
     ERROR
  ===================================================== */

  if (error) {
    return (
      <div className="page">

        <div className="page-header">
          <div>
            <h2>Dashboard</h2>

            <p>
              Welcome back to your financial
              command center.
            </p>
          </div>
        </div>

        <div className="dashboard-card dashboard-error">

          <div className="error-icon">
            !
          </div>

          <h3>
            Unable to load portfolio
          </h3>

          <p>
            {error}
          </p>

          <button
            type="button"
            onClick={() =>
              window.location.reload()
            }
          >
            Retry
          </button>

        </div>

      </div>
    )
  }


  if (!analytics) {
    return null
  }


  const totalPL =
    Number(
      analytics.total_profit_loss || 0
    )

  const totalReturn =
    Number(
      analytics.profit_loss_percentage || 0
    )


  /* =====================================================
     DASHBOARD
  ===================================================== */

  return (
    <div className="page dashboard-page">

      {/* =================================================
          HEADER
      ================================================= */}

      <div className="page-header dashboard-header">

        <div>
          <h2>
            Dashboard
          </h2>

          <p>
            Welcome back to your financial
            command center.
          </p>
        </div>

        <div className="dashboard-live">

          <span className="status-dot"></span>

          Portfolio synced

        </div>

      </div>


      {/* =================================================
          STAT CARDS
      ================================================= */}

      <section className="stats-grid dashboard-stats">

        <div className="stat-card">

          <div className="stat-card-top">

            <span>
              Portfolio Value
            </span>

            <span className="stat-icon">
              ◈
            </span>

          </div>

          <strong>
            {formatCurrency(
              analytics.total_current_value
            )}
          </strong>

          <small>
            Current market value
          </small>

        </div>


        <div className="stat-card">

          <div className="stat-card-top">

            <span>
              Total P&amp;L
            </span>

            <span className="stat-icon">
              $
            </span>

          </div>

          <strong
            className={
              getValueClass(totalPL)
            }
          >
            {formatCurrency(totalPL)}
          </strong>

          <small>
            Overall profit / loss
          </small>

        </div>


        <div className="stat-card">

          <div className="stat-card-top">

            <span>
              Total Return
            </span>

            <span className="stat-icon">
              %
            </span>

          </div>

          <strong
            className={
              getValueClass(totalReturn)
            }
          >
            {formatPercentage(
              totalReturn
            )}
          </strong>

          <small>
            Overall portfolio return
          </small>

        </div>


        <div className="stat-card">

          <div className="stat-card-top">

            <span>
              Portfolio Risk
            </span>

            <span className="stat-icon">
              !
            </span>

          </div>

          <strong>
            {Number(
              analytics.portfolio_risk_score
            ).toFixed(2)}
          </strong>

          <small
            className={
              getRiskClass(
                analytics.portfolio_risk_level
              )
            }
          >
            {analytics.portfolio_risk_level}
          </small>

        </div>

      </section>


      {/* =================================================
          OVERVIEW + HEALTH
      ================================================= */}

      <section className="dashboard-main-grid">

        {/* ===============================================
            PORTFOLIO OVERVIEW
        =============================================== */}

        <div className="dashboard-card overview-card">

          <div className="card-heading">

            <div>
              <h3>
                Portfolio Overview
              </h3>

              <p>
                Your current portfolio
                performance.
              </p>
            </div>

            <span className="card-label">
              LIVE
            </span>

          </div>


          <div className="overview-metrics">

            <div className="overview-metric">

              <span>
                Total Invested
              </span>

              <strong>
                {formatCurrency(
                  analytics.total_invested
                )}
              </strong>

            </div>


            <div className="overview-metric">

              <span>
                Current Value
              </span>

              <strong>
                {formatCurrency(
                  analytics.total_current_value
                )}
              </strong>

            </div>


            <div className="overview-metric">

              <span>
                Best Performer
              </span>

              <strong>
                {analytics.best_performer ||
                  'N/A'}
              </strong>

              {analytics.best_performer_return !==
                null && (
                <small
                  className={
                    getValueClass(
                      analytics.best_performer_return
                    )
                  }
                >
                  {formatPercentage(
                    analytics.best_performer_return
                  )}
                </small>
              )}

            </div>


            <div className="overview-metric">

              <span>
                Worst Performer
              </span>

              <strong>
                {analytics.worst_performer ||
                  'N/A'}
              </strong>

              {analytics.worst_performer_return !==
                null && (
                <small
                  className={
                    getValueClass(
                      analytics.worst_performer_return
                    )
                  }
                >
                  {formatPercentage(
                    analytics.worst_performer_return
                  )}
                </small>
              )}

            </div>

          </div>

        </div>


        {/* ===============================================
            PORTFOLIO HEALTH
        =============================================== */}

        <div className="dashboard-card health-card">

          <div className="card-heading">

            <div>
              <h3>
                Portfolio Health
              </h3>

              <p>
                Risk and allocation overview.
              </p>
            </div>

          </div>


          <div className="health-score">

            <div
              className={
                `risk-circle ${
                  getRiskClass(
                    analytics.portfolio_risk_level
                  )
                }`
              }
            >
              <strong>
                {Number(
                  analytics.portfolio_risk_score
                ).toFixed(0)}
              </strong>

              <span>
                Risk
              </span>
            </div>


            <div className="health-info">

              <span>
                Overall Risk
              </span>

              <strong>
                {analytics.portfolio_risk_level}
              </strong>

              <small>
                {analytics.diversification_level}
              </small>

            </div>

          </div>


          <div className="health-details">

            <div>
              <span>
                Highest Risk
              </span>

              <strong>
                {analytics.highest_risk_holding ||
                  'N/A'}
              </strong>

              <small>
                {Number(
                  analytics.highest_risk_score || 0
                ).toFixed(0)}{' '}
                ·{' '}
                {analytics.highest_risk_level ||
                  'N/A'}
              </small>
            </div>


            <div>
              <span>
                Largest Holding
              </span>

              <strong>
                {analytics.largest_holding ||
                  'N/A'}
              </strong>

              <small>
                {formatPercentage(
                  analytics.largest_allocation
                )}{' '}
                allocation
              </small>
            </div>

          </div>

        </div>

      </section>


      {/* =================================================
          OBSERVATIONS
      ================================================= */}

      <section className="dashboard-card insights-card">

        <div className="card-heading">

          <div>
            <h3>
              Portfolio Intelligence
            </h3>

            <p>
              Insights generated from your
              current portfolio data.
            </p>
          </div>

          <span className="ai-badge">
            AI
          </span>

        </div>


        <div className="insights-list">

          {analytics.observations?.length ? (

            analytics.observations.map(
              (observation, index) => (

                <div
                  className="insight-item"
                  key={`${observation}-${index}`}
                >

                  <span className="insight-icon">
                    !
                  </span>

                  <p>
                    {observation}
                  </p>

                </div>

              )
            )

          ) : (

            <div className="insight-item">

              <span className="insight-icon">
                ✓
              </span>

              <p>
                No major portfolio observations
                were generated.
              </p>

            </div>

          )}

        </div>

      </section>


      {/* =================================================
          HOLDINGS
      ================================================= */}

      <section className="dashboard-card holdings-card">

        <div className="card-heading">

          <div>
            <h3>
              Your Holdings
            </h3>

            <p>
              Current portfolio positions
              and risk.
            </p>
          </div>

          <span className="card-label">
            {analytics.holdings.length}{' '}
            {analytics.holdings.length === 1
              ? 'POSITION'
              : 'POSITIONS'}
          </span>

        </div>


        {analytics.holdings.length === 0 ? (

          <div className="empty-state">

            <h4>
              No holdings yet
            </h4>

            <p>
              Add stocks to your portfolio
              to see them here.
            </p>

          </div>

        ) : (

          <div className="holdings-table">

            <div className="holding-row holding-header">

              <span>
                Stock
              </span>

              <span>
                Qty
              </span>

              <span>
                Avg Price
              </span>

              <span>
                Current
              </span>

              <span>
                P&amp;L
              </span>

              <span>
                Return
              </span>

              <span>
                Risk
              </span>

            </div>


            {analytics.holdings.map(
              (holding) => (

                <div
                  className="holding-row"
                  key={holding.symbol}
                >

                  <div className="holding-name">

                    <strong>
                      {holding.symbol}
                    </strong>

                    <small>
                      {formatPercentage(
                        holding.allocation_percentage
                      )}{' '}
                      allocation
                    </small>

                  </div>


                  <span>
                    {holding.quantity}
                  </span>


                  <span>
                    {formatCurrency(
                      holding.average_price
                    )}
                  </span>


                  <span>
                    {formatCurrency(
                      holding.current_price
                    )}
                  </span>


                  <span
                    className={
                      getValueClass(
                        holding.profit_loss
                      )
                    }
                  >
                    {formatCurrency(
                      holding.profit_loss
                    )}
                  </span>


                  <span
                    className={
                      getValueClass(
                        holding.profit_loss_percentage
                      )
                    }
                  >
                    {formatPercentage(
                      holding.profit_loss_percentage
                    )}
                  </span>


                  <span
                    className={
                      `risk-badge ${
                        getRiskClass(
                          holding.risk_level
                        )
                      }`
                    }
                  >
                    {holding.risk_level}
                  </span>

                </div>

              )
            )}

          </div>

        )}

      </section>

    </div>
  )
}


export default Dashboard