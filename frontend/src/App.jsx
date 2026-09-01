/* oxlint-disable react(set-state-in-effect) */
import StockDetails from './pages/StockDetails'
import { useEffect, useState } from 'react'

import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from 'react-router-dom'

import Sidebar from './components/Sidebar'
import Topbar from './components/Topbar'

import Dashboard from './pages/Dashboard'
import Market from './pages/Market'
import Watchlist from './pages/Watchlist'
import AISignals from './pages/AISignals'
import PaperTrading from './pages/PaperTrading'
import Backtesting from './pages/Backtesting'
import Portfolio from './pages/Portfolio'
import Analytics from './pages/Analytics'
import News from './pages/News'
import Settings from './pages/Settings'

import './App.css'


const API_BASE_URL =
  'http://127.0.0.1:8000/api/v1'


/* =========================================================
   MAIN APPLICATION
========================================================= */

function App() {

  const [token, setToken] = useState(
    () =>
      localStorage.getItem(
        'finpilot_access_token'
      )
  )

  const [user, setUser] = useState(null)

  const [loading, setLoading] = useState(
    () =>
      Boolean(
        localStorage.getItem(
          'finpilot_access_token'
        )
      )
  )


  /* =======================================================
     AUTHENTICATION CHECK
  ======================================================= */

  useEffect(() => {

    if (!token) {
      return
    }

    let cancelled = false


    async function authenticateUser() {

      try {

        const response = await fetch(
          `${API_BASE_URL}/users/me`,
          {
            method: 'GET',

            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )


        if (!response.ok) {
          throw new Error(
            'Authentication failed'
          )
        }


        const data =
          await response.json()


        if (!cancelled) {

          setUser(data)

          setLoading(false)

        }

      } catch (error) {

        console.error(
          'Authentication error:',
          error
        )


        if (!cancelled) {

          localStorage.removeItem(
            'finpilot_access_token'
          )

          setToken(null)

          setUser(null)

          setLoading(false)

        }

      }

    }


    authenticateUser()


    return () => {
      cancelled = true
    }

  }, [token])


  /* =======================================================
     LOGIN
  ======================================================= */

  function handleLogin(newToken) {

    localStorage.setItem(
      'finpilot_access_token',
      newToken
    )

    setLoading(true)

    setToken(newToken)

  }


  /* =======================================================
     LOGOUT
  ======================================================= */

  function handleLogout() {

    localStorage.removeItem(
      'finpilot_access_token'
    )

    setToken(null)

    setUser(null)

    setLoading(false)

  }


  /* =======================================================
     LOADING SCREEN
  ======================================================= */

  if (loading) {

    return <LoadingScreen />

  }


  /* =======================================================
     APPLICATION
  ======================================================= */

  return (

    <BrowserRouter>

      {!token || !user ? (

        <LoginScreen
          onLogin={handleLogin}
        />

      ) : (

        <AuthenticatedApp
          user={user}
          onLogout={handleLogout}
        />

      )}

    </BrowserRouter>

  )

}


/* =========================================================
   AUTHENTICATED APPLICATION
========================================================= */

function AuthenticatedApp({
  user,
  onLogout,
}) {

  return (

    <div className="app-shell">

      {/* ================================================
          SIDEBAR
      ================================================= */}

      <Sidebar
        user={user}
        onLogout={onLogout}
      />


      {/* ================================================
          MAIN AREA
      ================================================= */}

      <div className="main-area">

        {/* TOPBAR */}

        <Topbar />


        {/* PAGE CONTENT */}

        <main className="main-content">

          <Routes>

            {/* ==========================================
                DASHBOARD
            ========================================== */}

            <Route
              path="/"
              element={<Dashboard />}
            />


            {/* ==========================================
                MARKET
            ========================================== */}

            <Route
              path="/market"
              element={<Market />}
            />
            <Route
              path="/market/:symbol"
              element={<StockDetails />}
            />

            {/* ==========================================
                WATCHLIST
            ========================================== */}

            <Route
              path="/watchlist"
              element={<Watchlist />}
            />


            {/* ==========================================
                AI SIGNALS
            ========================================== */}

            <Route
              path="/ai-signals"
              element={<AISignals />}
            />


            {/* ==========================================
                PAPER TRADING
            ========================================== */}

            <Route
              path="/paper-trading"
              element={<PaperTrading />}
            />


            {/* ==========================================
                BACKTESTING
            ========================================== */}

            <Route
              path="/backtesting"
              element={<Backtesting />}
            />


            {/* ==========================================
                PORTFOLIO
            ========================================== */}

            <Route
              path="/portfolio"
              element={<Portfolio />}
            />


            {/* ==========================================
                ANALYTICS
            ========================================== */}

            <Route
              path="/analytics"
              element={<Analytics />}
            />


            {/* ==========================================
                NEWS
            ========================================== */}

            <Route
              path="/news"
              element={<News />}
            />


            {/* ==========================================
                SETTINGS
            ========================================== */}

            <Route
              path="/settings"
              element={<Settings />}
            />


            {/* ==========================================
                UNKNOWN ROUTE
            ========================================== */}

            <Route
              path="*"
              element={
                <Navigate
                  to="/"
                  replace
                />
              }
            />

          </Routes>

        </main>

      </div>

    </div>

  )

}


/* =========================================================
   LOADING SCREEN
========================================================= */

function LoadingScreen() {

  return (

    <div className="loading-screen">

      <div className="loading-content">

        <div className="brand-logo">
          F
        </div>

        <h2>
          FinPilot AI
        </h2>

        <p>
          Loading your financial workspace...
        </p>

      </div>

    </div>

  )

}


/* =========================================================
   LOGIN SCREEN
========================================================= */

function LoginScreen({
  onLogin,
}) {

  const [email, setEmail] =
    useState('')

  const [password, setPassword] =
    useState('')

  const [error, setError] =
    useState('')

  const [loading, setLoading] =
    useState(false)


  /* =======================================================
     LOGIN FORM SUBMISSION
  ======================================================= */

  async function handleSubmit(event) {

    event.preventDefault()

    setError('')

    setLoading(true)


    try {

      const response = await fetch(
        `${API_BASE_URL}/users/login`,
        {
          method: 'POST',

          headers: {
            'Content-Type':
              'application/json',
          },

          body: JSON.stringify({
            email,
            password,
          }),
        }
      )


      const data =
        await response.json()


      /* ================================================
         LOGIN ERROR
      ================================================= */

      if (!response.ok) {

        throw new Error(
          data.detail ||
          'Login failed'
        )

      }


      /* ================================================
         SAVE TOKEN
      ================================================= */

      localStorage.setItem(
        'finpilot_access_token',
        data.access_token
      )


      /* ================================================
         UPDATE APPLICATION
      ================================================= */

      onLogin(
        data.access_token
      )

    } catch (error) {

      console.error(
        'Login error:',
        error
      )

      setError(
        error.message ||
        'Unable to login. Please try again.'
      )

      setLoading(false)

    }

  }


  /* =======================================================
     LOGIN UI
  ======================================================= */

  return (

    <div className="auth-screen">

      <div className="auth-card">

        {/* ================================================
            BRAND
        ================================================= */}

        <div className="auth-brand">

          <div className="brand-logo">
            F
          </div>

          <div>

            <h1>
              FINPILOT AI
            </h1>

            <p>
              Your AI Financial Copilot
            </p>

          </div>

        </div>


        {/* ================================================
            HEADING
        ================================================= */}

        <div className="auth-heading">

          <h2>
            Welcome Back
          </h2>

          <p>
            Sign in to continue to your
            financial dashboard.
          </p>

        </div>


        {/* ================================================
            LOGIN FORM
        ================================================= */}

        <form
          className="auth-form"
          onSubmit={handleSubmit}
        >

          {/* EMAIL */}

          <label htmlFor="email">
            Email
          </label>

          <input
            id="email"
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(event) =>
              setEmail(
                event.target.value
              )
            }
            required
          />


          {/* PASSWORD */}

          <label htmlFor="password">
            Password
          </label>

          <input
            id="password"
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(event) =>
              setPassword(
                event.target.value
              )
            }
            required
          />


          {/* ERROR */}

          {error && (

            <div className="auth-error">

              {error}

            </div>

          )}


          {/* LOGIN BUTTON */}

          <button
            type="submit"
            className="auth-submit"
            disabled={loading}
          >

            {loading
              ? 'Signing In...'
              : 'Sign In'}

          </button>

        </form>


        {/* ================================================
            REGISTER LINK
        ================================================= */}

        <div className="auth-footer">

          Don't have an account?

          <button
            type="button"
            className="auth-link"
          >
            Create Account
          </button>

        </div>

      </div>

    </div>

  )

}


export default App