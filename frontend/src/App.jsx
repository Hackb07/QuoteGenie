import { useState } from 'react'
import QuoteForm from './components/QuoteForm'
import { Hexagon } from 'lucide-react'

function App() {
  return (
    <div className="app-container">
      {/* Navbar to match the reference image */}
      <nav className="simple-nav">
        <div className="nav-logo">
          {/* Simple dots/logo representation */}
          <div className="dot-logo">
            <span className="dot"></span>
            <span className="dot"></span>
            <span className="dot"></span>
          </div>
        </div>
        <div className="nav-links">
          <a href="#" className="active">HOME</a>
          <a href="#">ABOUT</a>
          <a href="#">SERVICES</a>
          <a href="#">PORTFOLIO</a>
          <a href="#">CONTACT</a>
        </div>
        <div className="nav-menu-icon">
          <div className="bar"></div>
          <div className="bar"></div>
          <div className="bar"></div>
        </div>
      </nav>

      {/* Main Hero Content */}
      <main className="main-content">
        <div className="hero-text">
          <h1 className="simplicity-title">QUOTE GENIE</h1>
          <div className="subtitle-grid">
            <span>PREDICTIVE PRICING</span>
            <span>EASY TO NAVIGATE</span>
            <span>INSTANT QUOTES</span>
            <span>MORE PROFIT</span>
          </div>
        </div>

        <QuoteForm />
      </main>

      {/* Simple Footer/Icons area */}
      <footer className="simple-footer">
        <div className="footer-icon">★</div>
        <div className="footer-icon">📍</div>
        <div className="footer-icon">📄</div>
      </footer>
    </div>
  )
}

export default App
