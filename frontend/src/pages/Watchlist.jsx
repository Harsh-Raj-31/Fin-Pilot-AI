import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import {
  getWatchlist,
  addToWatchlist,
  removeFromWatchlist,
} from '../services/api'


function Watchlist() {
  const navigate = useNavigate()

  const [watchlist, setWatchlist] = useState([])
  const [symbol, setSymbol] = useState('')

  const [loading, setLoading] = useState(true)
  const [adding, setAdding] = useState(false)
  const [removing, setRemoving] = useState(null)

  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  /*
  =========================================================
  AUTHENTICATION
  =========================================================
  */

  const token = localStorage.getItem(
    'finpilot_access_token'
  )


  /*
  =========================================================
  LOAD WATCHLIST
  =========================================================
  */

  const loadWatchlist = async () => {
    try {
      setLoading(true)
      setError('')

      if (!token) {
        throw new Error(
          'Your session has expired. Please log in again.'
        )
      }

      const data = await getWatchlist(token)

      setWatchlist(
        Array.isArray(data) ? data : []
      )
    } catch (err) {
      setError(
        err.message ||
          'Failed to load watchlist.'
      )
    } finally {
      setLoading(false)
    }
  }


  /*
  =========================================================
  INITIAL LOAD
  =========================================================
  */

  useEffect(() => {
    loadWatchlist()
  }, [])


  /*
  =========================================================
  ADD STOCK
  =========================================================
  */

  const handleAdd = async (event) => {
    event.preventDefault()

    const cleanSymbol =
      symbol.trim().toUpperCase()

    setError('')
    setMessage('')

    if (!cleanSymbol) {
      setError(
        'Please enter a stock symbol.'
      )
      return
    }

    try {
      setAdding(true)

      if (!token) {
        throw new Error(
          'Your session has expired. Please log in again.'
        )
      }

      await addToWatchlist(
        cleanSymbol,
        token
      )

      setSymbol('')

      setMessage(
        `${cleanSymbol} added to your watchlist.`
      )

      await loadWatchlist()
    } catch (err) {
      setError(
        err.message ||
          'Failed to add stock to watchlist.'
      )
    } finally {
      setAdding(false)
    }
  }


  /*
  =========================================================
  REMOVE STOCK
  =========================================================
  */

  const handleRemove = async (
    stockSymbol
  ) => {
    setError('')
    setMessage('')

    try {
      setRemoving(stockSymbol)

      if (!token) {
        throw new Error(
          'Your session has expired. Please log in again.'
        )
      }

      await removeFromWatchlist(
        stockSymbol,
        token
      )

      setMessage(
        `${stockSymbol} removed from your watchlist.`
      )

      await loadWatchlist()
    } catch (err) {
      setError(
        err.message ||
          'Failed to remove stock.'
      )
    } finally {
      setRemoving(null)
    }
  }


  /*
  =========================================================
  QUICK VIEW
  =========================================================
  */

  const handleQuickView = (
    stockSymbol
  ) => {
    navigate(
      `/market/${stockSymbol}`
    )
  }


  /*
  =========================================================
  QUICK TRADE
  =========================================================
  */

  const handleQuickTrade = (
    stock
  ) => {
    if (
      stock.current_price === null ||
      stock.current_price === undefined
    ) {
      setError(
        `Current price for ${stock.symbol} is unavailable.`
      )
      return
    }

    navigate('/paper-trading', {
      state: {
        quickTrade: {
          symbol: stock.symbol,
          price: stock.current_price,
        },
      },
    })
  }


  /*
  =========================================================
  SIGNAL BADGE
  =========================================================
  */

  const getSignalClass = (
    signal
  ) => {
    if (!signal) {
      return 'watchlist-signal'
    }

    return `watchlist-signal watchlist-signal-${signal.toLowerCase()}`
  }


  /*
  =========================================================
  FORMAT PRICE
  =========================================================
  */

  const formatPrice = (
    price
  ) => {
    if (
      price === null ||
      price === undefined
    ) {
      return 'N/A'
    }

    return `₹${Number(price).toLocaleString(
      'en-IN',
      {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      }
    )}`
  }


  /*
  =========================================================
  FORMAT DAILY CHANGE
  =========================================================
  */

  const formatDailyChange = (
    change
  ) => {
    if (
      change === null ||
      change === undefined
    ) {
      return 'N/A'
    }

    const value = Number(change)

    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`
  }


  /*
  =========================================================
  RENDER
  =========================================================
  */

  return (
    <div className="watchlist-page">

      {/* =====================================================
          PAGE HEADER
      ===================================================== */}

      <div className="page-header">
        <h2>Watchlist</h2>

        <p>
          Track the stocks you are interested in.
        </p>
      </div>


      {/* =====================================================
          ADD STOCK
      ===================================================== */}

      <form
        onSubmit={handleAdd}
        className="watchlist-add-form"
      >
        <input
          type="text"
          value={symbol}
          onChange={(event) =>
            setSymbol(event.target.value)
          }
          placeholder="Enter stock symbol (e.g. TCS)"
          maxLength={20}
          disabled={adding}
        />

        <button
          type="submit"
          disabled={adding}
        >
          {adding
            ? 'Adding...'
            : 'Add Stock'}
        </button>
      </form>


      {/* =====================================================
          ERROR MESSAGE
      ===================================================== */}

      {error && (
        <div className="watchlist-message watchlist-error">
          {error}
        </div>
      )}


      {/* =====================================================
          SUCCESS MESSAGE
      ===================================================== */}

      {message && (
        <div className="watchlist-message watchlist-success">
          {message}
        </div>
      )}


      {/* =====================================================
          LOADING
      ===================================================== */}

      {loading && (
        <div className="watchlist-loading">
          <p>
            Loading watchlist...
          </p>
        </div>
      )}


      {/* =====================================================
          EMPTY STATE
      ===================================================== */}

      {!loading &&
        watchlist.length === 0 && (
          <div className="watchlist-empty">
            <h3>
              Your watchlist is empty
            </h3>

            <p>
              Add a stock to start
              tracking it.
            </p>
          </div>
        )}


      {/* =====================================================
          WATCHLIST
      ===================================================== */}

      {!loading &&
        watchlist.length > 0 && (
          <div className="watchlist-container">

            <div className="watchlist-table-wrapper">

              <table className="watchlist-table">

                {/* TABLE HEADER */}

                <thead>
                  <tr>
                    <th>Stock</th>
                    <th>Price</th>
                    <th>Daily Change</th>
                    <th>Signal</th>
                    <th>Confidence</th>
                    <th>Actions</th>
                  </tr>
                </thead>


                {/* TABLE BODY */}

                <tbody>

                  {watchlist.map(
                    (stock) => (
                      <tr
                        key={stock.symbol}
                      >

                        {/* STOCK */}

                        <td>
                          <div className="watchlist-stock">

                            <strong>
                              {stock.symbol}
                            </strong>

                            <span>
                              {
                                stock.company_name
                              }
                            </span>

                          </div>
                        </td>


                        {/* PRICE */}

                        <td>
                          <strong>
                            {formatPrice(
                              stock.current_price
                            )}
                          </strong>
                        </td>


                        {/* DAILY CHANGE */}

                        <td
                          className={
                            stock.daily_change !==
                              null &&
                            Number(
                              stock.daily_change
                            ) >= 0
                              ? 'watchlist-positive'
                              : 'watchlist-negative'
                          }
                        >
                          {formatDailyChange(
                            stock.daily_change
                          )}
                        </td>


                        {/* SIGNAL */}

                        <td>
                          <span
                            className={getSignalClass(
                              stock.signal
                            )}
                          >
                            {stock.signal ||
                              'N/A'}
                          </span>
                        </td>


                        {/* CONFIDENCE */}

                        <td>

                          {stock.confidence !==
                          null ? (
                            <div className="watchlist-confidence">

                              <span>
                                {
                                  stock.confidence
                                }
                                %
                              </span>

                              <div className="watchlist-confidence-bar">

                                <div
                                  style={{
                                    width: `${Math.min(
                                      Math.max(
                                        Number(
                                          stock.confidence
                                        ),
                                        0
                                      ),
                                      100
                                    )}%`,
                                  }}
                                />

                              </div>

                            </div>
                          ) : (
                            'N/A'
                          )}

                        </td>


                        {/* ACTIONS */}

                        <td>

                          <div className="watchlist-actions">

                            {/* QUICK VIEW */}

                            <button
                              type="button"
                              className="watchlist-view-button"
                              onClick={() =>
                                handleQuickView(
                                  stock.symbol
                                )
                              }
                            >
                              View
                            </button>


                            {/* QUICK TRADE */}

                            <button
                              type="button"
                              className="watchlist-trade-button"
                              disabled={
                                stock.current_price ===
                                  null ||
                                stock.current_price ===
                                  undefined
                              }
                              onClick={() =>
                                handleQuickTrade(
                                  stock
                                )
                              }
                            >
                              Trade
                            </button>


                            {/* REMOVE */}

                            <button
                              type="button"
                              className="watchlist-remove-button"
                              onClick={() =>
                                handleRemove(
                                  stock.symbol
                                )
                              }
                              disabled={
                                removing ===
                                stock.symbol
                              }
                            >
                              {removing ===
                              stock.symbol
                                ? 'Removing...'
                                : 'Remove'}
                            </button>

                          </div>

                        </td>

                      </tr>
                    )
                  )}

                </tbody>

              </table>

            </div>

          </div>
        )}
    </div>
  )
}

export default Watchlist