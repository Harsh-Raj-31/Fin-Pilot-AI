import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

const API_BASE_URL =
  'http://127.0.0.1:8000/api/v1'

function AISignals() {
  const navigate = useNavigate()

  const [stocks, setStocks] = useState([])
  const [analysis, setAnalysis] = useState({})
  const [marketCondition, setMarketCondition] =
    useState(null)

  const [selectedSymbol, setSelectedSymbol] =
    useState(null)

  const [explanation, setExplanation] =
    useState(null)

  const [loading, setLoading] = useState(true)
  const [explanationLoading, setExplanationLoading] =
    useState(false)

  const [error, setError] = useState('')
  const [explanationError, setExplanationError] =
    useState('')

  /*
   * =====================================================
   * LOAD STOCKS + AI ANALYSIS
   * =====================================================
   */

  useEffect(() => {
    let cancelled = false

    async function loadAIData() {
      try {
        setLoading(true)
        setError('')

        /*
         * Load available stocks.
         */

        const stocksResponse = await fetch(
          `${API_BASE_URL}/stocks?page=1&limit=50&sort_by=symbol&order=asc`
        )

        if (!stocksResponse.ok) {
          const data =
            await stocksResponse.json().catch(
              () => null
            )

          throw new Error(
            data?.detail ||
              'Unable to load stocks.'
          )
        }

        const stockData =
          await stocksResponse.json()

        if (cancelled) {
          return
        }

        setStocks(stockData)

        /*
         * Load market condition.
         */

        const marketResponse = await fetch(
          `${API_BASE_URL}/market/condition?period=3mo`
        )

        if (marketResponse.ok) {
          const marketData =
            await marketResponse.json()

          if (!cancelled) {
            setMarketCondition(
              marketData
            )
          }
        }

        /*
         * Load score + signal for every stock.
         */

        const analysisResults =
          await Promise.all(
            stockData.map(
              async (stock) => {
                try {
                  const [
                    scoreResponse,
                    signalResponse,
                  ] = await Promise.all([
                    fetch(
                      `${API_BASE_URL}/stocks/${stock.symbol}/score?period=3mo`
                    ),
                    fetch(
                      `${API_BASE_URL}/stocks/${stock.symbol}/signal?period=3mo`
                    ),
                  ])

                  const score =
                    scoreResponse.ok
                      ? await scoreResponse.json()
                      : null

                  const signal =
                    signalResponse.ok
                      ? await signalResponse.json()
                      : null

                  return [
                    stock.symbol,
                    {
                      score,
                      signal,
                    },
                  ]
                } catch (err) {
                  console.error(
                    `AI analysis failed for ${stock.symbol}:`,
                    err
                  )

                  return [
                    stock.symbol,
                    {
                      score: null,
                      signal: null,
                    },
                  ]
                }
              }
            )
          )

        if (cancelled) {
          return
        }

        const analysisMap = {}

        analysisResults.forEach(
          ([symbol, data]) => {
            analysisMap[symbol] =
              data
          }
        )

        setAnalysis(
          analysisMap
        )

        /*
         * Select first stock automatically.
         */

        if (
          stockData.length > 0
        ) {
          setSelectedSymbol(
            stockData[0].symbol
          )
        }

      } catch (err) {
        console.error(
          'AI Signals error:',
          err
        )

        if (!cancelled) {
          setError(
            err.message ||
              'Unable to load AI signals.'
          )
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    loadAIData()

    return () => {
      cancelled = true
    }
  }, [])


  /*
   * =====================================================
   * LOAD SELECTED STOCK EXPLANATION
   * =====================================================
   */

  useEffect(() => {
    let cancelled = false

    async function loadExplanation() {
      if (!selectedSymbol) {
        return
      }

      try {
        setExplanationLoading(true)
        setExplanationError('')
        setExplanation(null)

        const response = await fetch(
          `${API_BASE_URL}/stocks/${selectedSymbol}/explanation?period=3mo`
        )

        const data =
          await response.json()

        if (!response.ok) {
          throw new Error(
            data?.detail ||
              'Unable to load explanation.'
          )
        }

        if (!cancelled) {
          setExplanation(data)
        }

      } catch (err) {
        console.error(
          'Explanation error:',
          err
        )

        if (!cancelled) {
          setExplanationError(
            err.message ||
              'Unable to load explanation.'
          )
        }

      } finally {
        if (!cancelled) {
          setExplanationLoading(
            false
          )
        }
      }
    }

    loadExplanation()

    return () => {
      cancelled = true
    }
  }, [selectedSymbol])


  /*
   * =====================================================
   * HELPERS
   * =====================================================
   */

  function getSignalClass(signal) {
    const value =
      String(signal || '')
        .toLowerCase()

    if (
      value.includes('buy')
    ) {
      return 'positive'
    }

    if (
      value.includes('sell') ||
      value.includes('avoid')
    ) {
      return 'negative'
    }

    return ''
  }


  function getScoreClass(score) {
    if (
      score === null ||
      score === undefined
    ) {
      return ''
    }

    if (score >= 70) {
      return 'positive'
    }

    if (score < 40) {
      return 'negative'
    }

    return ''
  }


  function getScore(data) {
    return (
      data?.score?.overall_score ??
      null
    )
  }


  function getSignal(data) {
    return (
      data?.signal?.signal ??
      'N/A'
    )
  }


  function getConfidence(data) {
    return (
      data?.signal?.confidence ??
      null
    )
  }


  function formatConfidence(value) {
    if (
      value === null ||
      value === undefined
    ) {
      return 'N/A'
    }

    return `${Number(value).toFixed(2)}%`
  }


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


  /*
   * =====================================================
   * LOADING
   * =====================================================
   */

  if (loading) {
    return (
      <div className="page ai-signals-page">

        <div className="page-header">

          <div>

            <h2>
              AI Signals
            </h2>

            <p>
              Explore FinPilot's
              AI-powered stock signals.
            </p>

          </div>

        </div>

        <div className="market-loading">

          FinPilot AI is analyzing
          the market...

        </div>

      </div>
    )
  }


  /*
   * =====================================================
   * ERROR
   * =====================================================
   */

  if (error) {
    return (
      <div className="page ai-signals-page">

        <div className="page-header">

          <div>

            <h2>
              AI Signals
            </h2>

            <p>
              Explore FinPilot's
              AI-powered stock signals.
            </p>

          </div>

        </div>

        <div className="market-error">

          <strong>
            Unable to load AI signals
          </strong>

          <span>
            {error}
          </span>

        </div>

      </div>
    )
  }


  const selectedStock =
    stocks.find(
      (stock) =>
        stock.symbol ===
        selectedSymbol
    )

  const selectedAnalysis =
    selectedSymbol
      ? analysis[selectedSymbol]
      : null

  const selectedScore =
    getScore(
      selectedAnalysis
    )

  const selectedSignal =
    getSignal(
      selectedAnalysis
    )

  const selectedConfidence =
    getConfidence(
      selectedAnalysis
    )


  /*
   * =====================================================
   * MAIN PAGE
   * =====================================================
   */

  return (
    <div className="page ai-signals-page">

      {/* =================================================
          HEADER
      ================================================= */}

      <div className="page-header">

        <div>

          <h2>
            AI Signals
          </h2>

          <p>
            Explore FinPilot's
            AI-powered stock signals.
          </p>

        </div>


        <div className="ai-online-status">

          <span className="status-dot"></span>

          AI Engine Online

        </div>

      </div>


      {/* =================================================
          MARKET INTELLIGENCE
      ================================================= */}

      <section className="dashboard-card ai-market-card">

        <div>

          <span className="section-eyebrow">
            MARKET INTELLIGENCE
          </span>

          <h3>
            Current Market Condition
          </h3>

          <p>
            FinPilot combines market
            conditions with stock-level
            analysis to generate signals.
          </p>

        </div>


        <div className="ai-market-metrics">

          <div>

            <span>
              Market Trend
            </span>

            <strong>
              {marketCondition?.trend ||
                'N/A'}
            </strong>

          </div>


          <div>

            <span>
              Market Strength
            </span>

            <strong>
              {marketCondition?.market_strength ??
                'N/A'}
            </strong>

          </div>


          <div>

            <span>
              Analysis Period
            </span>

            <strong>
              3 Months
            </strong>

          </div>

        </div>

      </section>


      {/* =================================================
          AI SIGNAL TABLE
      ================================================= */}

      <section className="dashboard-card ai-signals-table-card">

        <div className="card-heading">

          <div>

            <h3>
              AI Stock Signals
            </h3>

            <p>
              Signals generated from
              FinPilot's scoring engine.
            </p>

          </div>


          <span className="card-label">

            {stocks.length}{' '}

            {stocks.length === 1
              ? 'STOCK'
              : 'STOCKS'}

          </span>

        </div>


        <div className="ai-signals-table">

          {/* HEADER */}

          <div className="ai-signal-row ai-signal-header">

            <span>
              Stock
            </span>

            <span>
              Signal
            </span>

            <span>
              Score
            </span>

            <span>
              Confidence
            </span>

            <span>
              Action
            </span>

          </div>


          {/* STOCKS */}

          {stocks.map(
            (stock) => {

              const stockAnalysis =
                analysis[
                  stock.symbol
                ]

              const score =
                getScore(
                  stockAnalysis
                )

              const signal =
                getSignal(
                  stockAnalysis
                )

              const confidence =
                getConfidence(
                  stockAnalysis
                )

              return (

                <button
                  type="button"
                  key={
                    stock.symbol
                  }
                  className={`ai-signal-row ${
                    selectedSymbol ===
                    stock.symbol
                      ? 'selected'
                      : ''
                  }`}
                  onClick={() =>
                    setSelectedSymbol(
                      stock.symbol
                    )
                  }
                >

                  {/* STOCK */}

                  <span className="ai-stock-cell">

                    <strong>
                      {stock.symbol}
                    </strong>

                    <small>
                      {stock.company_name}
                    </small>

                  </span>


                  {/* SIGNAL */}

                  <span
                    className={
                      getSignalClass(
                        signal
                      )
                    }
                  >
                    {signal}
                  </span>


                  {/* SCORE */}

                  <span
                    className={
                      getScoreClass(
                        score
                      )
                    }
                  >
                    {score === null
                      ? 'N/A'
                      : `${Number(score).toFixed(1)}/100`}
                  </span>


                  {/* CONFIDENCE */}

                  <span>
                    {formatConfidence(
                      confidence
                    )}
                  </span>


                  {/* ACTION */}

                  <span>

                    <span className="view-signal-button">
                      View
                    </span>

                  </span>

                </button>
              )
            }
          )}

        </div>

      </section>


      {/* =================================================
          SELECTED STOCK ANALYSIS
      ================================================= */}

      {selectedStock && (

        <section className="ai-detail-grid">

          {/* =================================================
              SCORE BREAKDOWN
          ================================================= */}

          <div className="dashboard-card">

            <div className="card-heading">

              <div>

                <span className="section-eyebrow">
                  SELECTED STOCK
                </span>

                <h3>
                  {selectedStock.symbol}
                </h3>

                <p>
                  {selectedStock.company_name}
                </p>

              </div>


              <button
                type="button"
                className="view-details-button"
                onClick={() =>
                  navigate(
                    `/market/${selectedStock.symbol}`
                  )
                }
              >
                Full Analysis
              </button>

            </div>


            <div className="selected-signal-summary">

              <div>

                <span>
                  AI Signal
                </span>

                <strong
                  className={
                    getSignalClass(
                      selectedSignal
                    )
                  }
                >
                  {selectedSignal}
                </strong>

              </div>


              <div>

                <span>
                  Overall Score
                </span>

                <strong
                  className={
                    getScoreClass(
                      selectedScore
                    )
                  }
                >
                  {selectedScore ===
                  null
                    ? 'N/A'
                    : `${Number(selectedScore).toFixed(1)}/100`}
                </strong>

              </div>


              <div>

                <span>
                  Confidence
                </span>

                <strong>
                  {formatConfidence(
                    selectedConfidence
                  )}
                </strong>

              </div>

            </div>


            {/* SCORE BREAKDOWN */}

            <div className="ai-score-breakdown">

              <div>

                <span>
                  Performance
                </span>

                <strong>
                  {selectedAnalysis?.score?.performance_score ??
                    'N/A'}
                </strong>

              </div>


              <div>

                <span>
                  Technical
                </span>

                <strong>
                  {selectedAnalysis?.score?.technical_score ??
                    'N/A'}
                </strong>

              </div>


              <div>

                <span>
                  Risk
                </span>

                <strong>
                  {selectedAnalysis?.score?.risk_score ??
                    'N/A'}
                </strong>

              </div>


              <div>

                <span>
                  Strength
                </span>

                <strong>
                  {selectedAnalysis?.score?.strength ??
                    'N/A'}
                </strong>

              </div>

            </div>


            <div className="selected-stock-price">

              <span>
                Current Price
              </span>

              <strong>
                {formatCurrency(
                  selectedStock.current_price
                )}
              </strong>

            </div>

          </div>


          {/* =================================================
              EXPLANATION
          ================================================= */}

          <div className="dashboard-card">

            <div className="card-heading">

              <div>

                <span className="section-eyebrow">
                  AI EXPLANATION
                </span>

                <h3>
                  Why {selectedSignal}?
                </h3>

              </div>

            </div>


            {explanationLoading ? (

              <div className="explanation-loading">

                FinPilot AI is preparing
                the explanation...

              </div>

            ) : explanationError ? (

              <div className="market-error">

                {explanationError}

              </div>

            ) : explanation ? (

              <div className="ai-explanation">

                <p>
                  {explanation.summary}
                </p>


                {explanation.reasons?.length > 0 && (

                  <div className="ai-reasons">

                    <span>
                      Key Factors
                    </span>

                    <ul>

                      {explanation.reasons.map(
                        (reason, index) => (

                          <li
                            key={`${selectedSymbol}-reason-${index}`}
                          >
                            {reason}
                          </li>

                        )
                      )}

                    </ul>

                  </div>

                )}

              </div>

            ) : (

              <div className="explanation-loading">

                No explanation available.

              </div>

            )}

          </div>

        </section>

      )}


      {/* =================================================
          FOOTER
      ================================================= */}

      <div className="market-footer-note">

        <span className="status-dot"></span>

        AI signals are generated using
        FinPilot's scoring model,
        technical indicators, risk
        metrics and market conditions.

      </div>

    </div>
  )
}

export default AISignals