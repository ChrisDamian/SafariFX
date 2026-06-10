import { useEffect } from 'react'
import RateDashboard from './RateDashboard'
import ReasoningTrace from './ReasoningTrace'
import RecommendationReport from './RecommendationReport'

export default function AnalysisView({ invoices, rates, report, isAnalyzing, onRunAnalysis, fetchRates }) {
  useEffect(() => {
    if (rates.length === 0) fetchRates()
  }, [rates, fetchRates])

  const totalExposure = invoices.reduce((s, i) => s + (i.amount_usd || 0), 0)

  return (
    <div className="animate-in">
      <div className="page-header">
        <h1>FX Analysis Engine</h1>
        <p>Multi-step reasoning powered by Microsoft Foundry IQ — grounded, cited, zero-hallucination treasury intelligence</p>
      </div>

      {/* Pre-Analysis Summary */}
      {!report && (
        <div className="glass-card glass-card--static" style={{ marginBottom: 'var(--space-2xl)' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 'var(--space-md)' }}>
            <div>
              <h3 style={{ marginBottom: 'var(--space-xs)' }}>Ready for Analysis</h3>
              <div style={{ color: 'var(--text-secondary)', fontSize: 'var(--font-size-sm)' }}>
                <span className="mono" style={{ color: 'var(--accent-primary)' }}>{invoices.length}</span> invoices loaded •{' '}
                <span className="mono" style={{ color: 'var(--accent-primary)' }}>${totalExposure.toLocaleString()}</span> total USD exposure •{' '}
                <span className="mono" style={{ color: 'var(--accent-primary)' }}>{rates.length}</span> bank rates tracked
              </div>
            </div>
            <button
              className={`btn btn--primary btn--lg ${isAnalyzing ? 'btn--loading' : ''}`}
              onClick={onRunAnalysis}
              disabled={isAnalyzing || invoices.length === 0}
              id="run-analysis-btn"
            >
              {isAnalyzing ? 'Analyzing...' : '🧠 Run SafariFX Analysis'}
            </button>
          </div>

          {invoices.length === 0 && (
            <div style={{ marginTop: 'var(--space-md)', padding: 'var(--space-md)', background: 'hsla(38, 92%, 55%, 0.08)', border: '1px solid hsla(38, 92%, 55%, 0.15)', borderRadius: 'var(--radius-sm)' }}>
              <span style={{ color: 'var(--accent-warning)' }}>⚠️ No invoices loaded. Go to Upload Invoices first.</span>
            </div>
          )}
        </div>
      )}

      {/* Loading State */}
      {isAnalyzing && (
        <div className="glass-card glass-card--static" style={{ textAlign: 'center', padding: 'var(--space-3xl)' }}>
          <div style={{ fontSize: '3rem', marginBottom: 'var(--space-md)', animation: 'pulse 2s ease-in-out infinite' }}>🧠</div>
          <h3 style={{ color: 'var(--accent-primary)', marginBottom: 'var(--space-sm)' }}>Running Multi-Step Analysis...</h3>
          <p style={{ color: 'var(--text-muted)', fontSize: 'var(--font-size-sm)' }}>
            Querying Foundry IQ knowledge base for CBK policy, bank tariffs, and market intelligence
          </p>
          <div style={{ marginTop: 'var(--space-lg)', display: 'flex', justifyContent: 'center', gap: 'var(--space-sm)' }}>
            {[1, 2, 3, 4, 5, 6].map(n => (
              <div key={n} style={{
                width: 10, height: 10,
                borderRadius: '50%',
                background: 'var(--accent-primary)',
                opacity: 0.3,
                animation: `pulse 1.5s ease-in-out infinite`,
                animationDelay: `${n * 0.15}s`,
              }} />
            ))}
          </div>
        </div>
      )}

      {/* Results */}
      {report && !isAnalyzing && (
        <>
          {/* Current Rates */}
          <div className="section-divider">
            <div className="section-divider__line" />
            <span className="section-divider__text">Market Rates Snapshot</span>
            <div className="section-divider__line" />
          </div>
          <RateDashboard rates={report.rates_snapshot || rates} />

          {/* Reasoning Trace */}
          <div className="section-divider">
            <div className="section-divider__line" />
            <span className="section-divider__text">Reasoning Trace — 6-Step Analysis</span>
            <div className="section-divider__line" />
          </div>
          <ReasoningTrace steps={report.reasoning_steps} isActive={false} />

          {/* Recommendations */}
          <div className="section-divider" style={{ marginTop: 'var(--space-2xl)' }}>
            <div className="section-divider__line" />
            <span className="section-divider__text">Cited Recommendations</span>
            <div className="section-divider__line" />
          </div>
          <RecommendationReport report={report} />

          {/* Re-run */}
          <div style={{ textAlign: 'center', marginTop: 'var(--space-xl)' }}>
            <button className="btn btn--secondary" onClick={onRunAnalysis} id="rerun-analysis-btn">
              🔄 Re-run Analysis with Latest Rates
            </button>
          </div>
        </>
      )}
    </div>
  )
}
