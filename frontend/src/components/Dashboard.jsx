import { useEffect } from 'react'
import RateDashboard from './RateDashboard'
import SavingsTracker from './SavingsTracker'

export default function Dashboard({ rates, invoices, analysisReport, fetchRates }) {
  useEffect(() => {
    fetchRates()
  }, [fetchRates])

  const totalInvoiceValue = invoices.reduce((sum, inv) => sum + (inv.amount_usd || 0), 0)
  const urgentCount = invoices.filter(inv => inv.urgency === 'urgent' || inv.urgency === 'high').length

  return (
    <div className="animate-in">
      {/* Page Header */}
      <div className="page-header">
        <h1>FX Intelligence Dashboard</h1>
        <p>Real-time multi-bank exchange rate monitoring and treasury optimization for the Kenyan market</p>
      </div>

      {/* Stats Overview */}
      <div className="grid-3 stagger-children" style={{ marginBottom: 'var(--space-2xl)' }}>
        <div className="glass-card stat-card">
          <div className="stat-card__value">{invoices.length}</div>
          <div className="stat-card__label">Pending Invoices</div>
        </div>
        <div className="glass-card stat-card">
          <div className="stat-card__value" style={{ color: 'var(--accent-primary)' }}>
            ${totalInvoiceValue.toLocaleString()}
          </div>
          <div className="stat-card__label">Total USD Exposure</div>
        </div>
        <div className="glass-card stat-card">
          <div className="stat-card__value" style={{ color: urgentCount > 0 ? 'var(--accent-warning)' : 'var(--accent-success)' }}>
            {urgentCount}
          </div>
          <div className="stat-card__label">Urgent Actions</div>
        </div>
      </div>

      {/* Rates Section */}
      <div className="section-divider">
        <div className="section-divider__line" />
        <span className="section-divider__text">Live Interbank Rates — KES/USD</span>
        <div className="section-divider__line" />
      </div>

      <RateDashboard rates={rates} />

      {/* Savings Section */}
      {analysisReport && (
        <>
          <div className="section-divider">
            <div className="section-divider__line" />
            <span className="section-divider__text">Cumulative Savings</span>
            <div className="section-divider__line" />
          </div>
          <SavingsTracker report={analysisReport} />
        </>
      )}

      {/* Empty State */}
      {invoices.length === 0 && (
        <div className="glass-card glass-card--static" style={{ textAlign: 'center', marginTop: 'var(--space-2xl)', padding: 'var(--space-3xl)' }}>
          <div style={{ fontSize: '3rem', marginBottom: 'var(--space-md)', opacity: 0.5 }}>📄</div>
          <h3 style={{ color: 'var(--text-secondary)', marginBottom: 'var(--space-sm)' }}>No Invoices Loaded</h3>
          <p style={{ color: 'var(--text-muted)', fontSize: 'var(--font-size-sm)' }}>
            Navigate to <strong>Upload Invoices</strong> to import your pending USD invoices and start optimizing your FX purchases.
          </p>
        </div>
      )}
    </div>
  )
}
