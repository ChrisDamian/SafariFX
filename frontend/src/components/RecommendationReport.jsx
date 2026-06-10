export default function RecommendationReport({ report }) {
  if (!report) return null

  const { recommendations, total_savings_kes, total_savings_pct } = report

  return (
    <div className="animate-in" id="recommendation-report">
      {/* Savings Header */}
      <div className="glass-card glass-card--static savings-summary" style={{ marginBottom: 'var(--space-2xl)' }}>
        <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.12em', marginBottom: 'var(--space-sm)' }}>
          Projected Total Savings
        </div>
        <div className="savings-summary__value">
          KES {(total_savings_kes || 0).toLocaleString()}
        </div>
        <div className="savings-summary__pct">
          ↓ {(total_savings_pct || 0).toFixed(1)}% vs worst-case execution
        </div>
        <div style={{ color: 'var(--text-muted)', fontSize: 'var(--font-size-sm)', marginTop: 'var(--space-md)' }}>
          Compared to executing all purchases at the widest-spread bank at peak rates
        </div>
      </div>

      {/* Recommendations */}
      <div className="section-divider">
        <div className="section-divider__line" />
        <span className="section-divider__text">Execution Recommendations</span>
        <div className="section-divider__line" />
      </div>

      {(recommendations || []).map((rec, i) => (
        <div className="recommendation" key={i} id={`recommendation-${i}`}>
          <div className="recommendation__header">
            <div>
              <div className="recommendation__bank">
                {rec.bank_name}
              </div>
              <div style={{ color: 'var(--text-muted)', fontSize: 'var(--font-size-xs)' }}>
                {rec.timing}
              </div>
            </div>
            <div className="recommendation__amount">
              ${(rec.amount_usd || 0).toLocaleString()}
            </div>
          </div>

          <div className="recommendation__detail">
            <span className="recommendation__detail-label">Exchange Rate</span>
            <span className="mono" style={{ fontWeight: 600 }}>KES {rec.rate?.toFixed(2)}</span>
          </div>

          <div className="recommendation__detail">
            <span className="recommendation__detail-label">Total Cost</span>
            <span className="mono" style={{ fontWeight: 600 }}>KES {(rec.total_kes || 0).toLocaleString()}</span>
          </div>

          <div className="recommendation__detail" style={{ border: 'none' }}>
            <span className="recommendation__detail-label">Rationale</span>
            <span style={{ color: 'var(--text-secondary)', fontSize: 'var(--font-size-sm)' }}>{rec.rationale}</span>
          </div>

          {/* Savings */}
          <div className="recommendation__savings">
            <span>💰</span>
            <div>
              <span style={{ color: 'var(--text-muted)', fontSize: 'var(--font-size-xs)' }}>Savings vs worst option: </span>
              <span className="recommendation__savings-value">
                KES {(rec.savings_vs_worst || 0).toLocaleString()}
              </span>
            </div>
          </div>

          {/* Citations */}
          {rec.citations && rec.citations.length > 0 && (
            <div className="recommendation__citations">
              <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--text-muted)', marginBottom: 'var(--space-xs)' }}>
                📎 Grounding Sources:
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--space-xs)' }}>
                {rec.citations.map((cite, j) => (
                  <span className="recommendation__citation-tag" key={j}>
                    {cite}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
