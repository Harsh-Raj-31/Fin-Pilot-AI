import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

const API_BASE_URL =
  'http://127.0.0.1:8000/api/v1'

function Market() {
  const navigate = useNavigate()

  const [stocks, setStocks] = useState([])
  const [marketCondition, setMarketCondition] =
    useState(null)

  const [search, setSearch] = useState('')
  const [exchange, setExchange] = useState('')
  const [sector, setSector] = useState('')

  const [loading, setLoading] = useState(true)
  const [marketLoading, setMarketLoading] =
    useState(true)

  const [error, setError] = useState('')
  const [marketError, setMarketError] =
    useState('')

  /* =====================================================
     FETCH STOCKS
  ===================================================== */

  useEffect(() => {
    let cancelled = false

    async function fetchStocks() {
      try {
        setLoading(true)
        setError('')

        const params = new URLSearchParams({
          page: '1',
          limit: '50',
          sort_by: 'symbol',
          order: 'asc',
        })

        if (search.trim()) {
          params.set(
            'search',
            search.trim()
          )
        }

        if (exchange) {
          params.set(
            'exchange',
            exchange
          )
        }

        if (sector) {
          params.set(
            'sector',
            sector
          )
        }

        const response = await fetch(
          `${API_BASE_URL}/stocks?${params.toString()}`
        )

        if (!response.ok) {
          const data =
            await response.json().catch(
              () => null
            )

          throw new Error(
            data?.detail ||
              'Unable to load stocks.'
          )
        }

        const data =
          await response.json()

        if (!cancelled) {
          setStocks(data)
        }
      } catch (err) {
        console.error(
          'Stock fetch error:',
          err
        )

        if (!cancelled) {
          setError(
            err.message ||
              'Unable to load stocks.'
          )
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    fetchStocks()

    return () => {
      cancelled = true
    }
  }, [search, exchange, sector])


  /* =====================================================
     FETCH MARKET CONDITION
  ===================================================== */

  useEffect(() => {
    let cancelled = false

    async function fetchMarketCondition() {
      try {
        setMarketLoading(true)
        setMarketError('')

        const response = await fetch(
          `${API_BASE_URL}/market/condition?period=3mo`
        )

        if (!response.ok) {
          const data =
            await response.json().catch(
              () => null
            )

          throw new Error(
            data?.detail ||
              'Unable to load market condition.'
          )
        }

        const data =
          await response.json()

        if (!cancelled) {
          setMarketCondition(data)
        }
      } catch (err) {
        console.error(
          'Market condition error:',
          err
        )

        if (!cancelled) {
          setMarketError(
            err.message ||
              'Unable to load market condition.'
          )
        }
      } finally {
        if (!cancelled) {
          setMarketLoading(false)
        }
      }
    }

    fetchMarketCondition()

    return () => {
      cancelled = true
    }
  }, [])


  /* =====================================================
     FORMATTERS
  ===================================================== */

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


  function formatNumber(value) {
    if (
      value === null ||
      value === undefined
    ) {
      return '—'
    }

    return Number(value).toLocaleString(
      'en-IN'
    )
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


  function getPriceChange(stock) {
    if (
      stock.previous_close === null ||
      stock.previous_close === undefined ||
      !stock.previous_close
    ) {
      return null
    }

    return (
      (
        (stock.current_price -
          stock.previous_close) /
        stock.previous_close
      ) * 100
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


  function getMarketTrendClass(trend) {
    const value = String(
      trend || ''
    ).toLowerCase()

    if (
      value.includes('bull') ||
      value.includes('up')
    ) {
      return 'positive'
    }

    if (
      value.includes('bear') ||
      value.includes('down')
    ) {
      return 'negative'
    }

    return ''
  }


  /* =====================================================
     OPEN STOCK DETAILS
  ===================================================== */

  function openStockDetails(symbol) {
    navigate(
      `/market/${symbol}`
    )
  }


  /* =====================================================
     LOADING STATE
  ===================================================== */

  if (
    loading &&
    stocks.length === 0
  ) {
    return (
      <div className="page market-page">

        <div className="page-header">
          <div>
            <h2>Market</h2>

            <p>
              Explore market intelligence
              and stock data.
            </p>
          </div>
        </div>

        <div className="market-loading">
          Loading market data...
        </div>

      </div>
    )
  }


  /* =====================================================
     MAIN PAGE
  ===================================================== */

  return (
    <div className="page market-page">

      {/* =================================================
          HEADER
      ================================================= */}

      <div className="page-header market-header">

        <div>
          <h2>
            Market
          </h2>

          <p>
            Explore market intelligence
            and stock data.
          </p>
        </div>

        <div className="market-live">

          <span className="status-dot"></span>

          Market Data

        </div>

      </div>


      {/* =================================================
          MARKET CONDITION
      ================================================= */}

      <section className="market-condition-card">

        <div className="market-condition-heading">

          <div>

            <span className="section-eyebrow">
              MARKET INTELLIGENCE
            </span>

            <h3>
              NIFTY 50 Market Condition
            </h3>

            <p>
              Current market trend based
              on historical market data.
            </p>

          </div>


          <div className="market-condition-status">

            {marketLoading ? (

              <span>
                Loading...
              </span>

            ) : marketError ? (

              <span className="negative">
                Unavailable
              </span>

            ) : (

              <span
                className={
                  getMarketTrendClass(
                    marketCondition?.trend
                  )
                }
              >
                {marketCondition?.trend ||
                  'NEUTRAL'}
              </span>

            )}

          </div>

        </div>


        {!marketLoading &&
          !marketError &&
          marketCondition && (

            <div className="market-condition-metrics">

              <div>

                <span>
                  Trend
                </span>

                <strong
                  className={
                    getMarketTrendClass(
                      marketCondition.trend
                    )
                  }
                >
                  {marketCondition.trend ||
                    'N/A'}
                </strong>

              </div>


              <div>

                <span>
                  Strength
                </span>

                <strong>
                  {marketCondition.strength ??
                    'N/A'}
                </strong>

              </div>


              <div>

                <span>
                  Period
                </span>

                <strong>
                  3 Months
                </strong>

              </div>

            </div>

          )}

      </section>


      {/* =================================================
          SEARCH + FILTERS
      ================================================= */}

      <section className="market-toolbar">

        <div className="market-search">

          <span>
            ⌕
          </span>

          <input
            type="text"
            placeholder="Search by company name..."
            value={search}
            onChange={(event) =>
              setSearch(
                event.target.value
              )
            }
          />

          {search && (

            <button
              type="button"
              onClick={() =>
                setSearch('')
              }
              aria-label="Clear search"
            >
              ×
            </button>

          )}

        </div>


        <select
          value={exchange}
          onChange={(event) =>
            setExchange(
              event.target.value
            )
          }
        >

          <option value="">
            All Exchanges
          </option>

          <option value="NSE">
            NSE
          </option>

          <option value="BSE">
            BSE
          </option>

        </select>


        <select
          value={sector}
          onChange={(event) =>
            setSector(
              event.target.value
            )
          }
        >

          <option value="">
            All Sectors
          </option>

          <option value="Information Technology">
            Information Technology
          </option>

          <option value="Banking">
            Banking
          </option>

          <option value="Financial Services">
            Financial Services
          </option>

          <option value="Energy">
            Energy
          </option>

          <option value="Healthcare">
            Healthcare
          </option>

          <option value="Consumer">
            Consumer
          </option>

        </select>

      </section>


      {/* =================================================
          ERROR
      ================================================= */}

      {error && (

        <div className="market-error">

          <strong>
            Unable to load stocks
          </strong>

          <span>
            {error}
          </span>

        </div>

      )}


      {/* =================================================
          STOCK TABLE
      ================================================= */}

      <section className="dashboard-card market-stocks-card">

        <div className="card-heading">

          <div>

            <h3>
              Market Stocks
            </h3>

            <p>
              Browse available stocks and
              current market prices.
            </p>

          </div>


          <span className="card-label">

            {stocks.length}{' '}

            {stocks.length === 1
              ? 'STOCK'
              : 'STOCKS'}

          </span>

        </div>


        {stocks.length === 0 && !loading ? (

          <div className="empty-state">

            <h4>
              No stocks found
            </h4>

            <p>
              Try changing your search
              or filters.
            </p>

          </div>

        ) : (

          <div className="market-table">

            {/* TABLE HEADER */}

            <div className="market-row market-table-header">

              <span>
                Stock
              </span>

              <span>
                Exchange
              </span>

              <span>
                Sector
              </span>

              <span>
                Price
              </span>

              <span>
                Change
              </span>

              <span>
                Day High
              </span>

              <span>
                Day Low
              </span>

              <span>
                Volume
              </span>

            </div>


            {/* STOCK ROWS */}

            {stocks.map(
              (stock) => {

                const change =
                  getPriceChange(
                    stock
                  )

                return (

                  <div
                    className="market-row"
                    key={stock.symbol}
                  >

                    {/* STOCK */}

                    <button
                      type="button"
                      className="market-stock-name stock-link"
                      onClick={() =>
                        openStockDetails(
                          stock.symbol
                        )
                      }
                      title={`View ${stock.symbol} analysis`}
                    >

                      <strong>
                        {stock.symbol}
                      </strong>

                      <small>
                        {stock.company_name}
                      </small>

                    </button>


                    {/* EXCHANGE */}

                    <span>
                      {stock.exchange ||
                        '—'}
                    </span>


                    {/* SECTOR */}

                    <span className="market-sector">

                      {stock.sector ||
                        '—'}

                    </span>


                    {/* PRICE */}

                    <strong>

                      {formatCurrency(
                        stock.current_price
                      )}

                    </strong>


                    {/* CHANGE */}

                    <span
                      className={
                        getValueClass(
                          change
                        )
                      }
                    >

                      {change === null
                        ? '—'
                        : formatPercentage(
                            change
                          )}

                    </span>


                    {/* DAY HIGH */}

                    <span>

                      {formatCurrency(
                        stock.day_high
                      )}

                    </span>


                    {/* DAY LOW */}

                    <span>

                      {formatCurrency(
                        stock.day_low
                      )}

                    </span>


                    {/* VOLUME */}

                    <span>

                      {formatNumber(
                        stock.volume
                      )}

                    </span>

                  </div>

                )
              }
            )}

          </div>

        )}

      </section>


      {/* =================================================
          FOOTER NOTE
      ================================================= */}

      <div className="market-footer-note">

        <span className="status-dot"></span>

        Select any stock to view detailed
        FinPilot analysis, technical indicators,
        risk and AI signals.

      </div>

    </div>
  )
}

export default Market