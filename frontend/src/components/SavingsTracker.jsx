export default function SavingsTracker({ report }) {
  if (!report) return null

  const { total_savings_kes, total_savings_pct, recommendations } = report

  // Build a simple bar chart of savings per recommendation
  const maxSavings = Math.max(...(recommendations || []).map(r => r.savings_vs_worst || 0), 1)

  return (
    <div className="glass-card glass-card--static animate-in" id="savings-tracker">
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--space-xl)' }}>
        <div>
          <h3 style={{ marginBottom: 'var(--space-xs)' }}>Savings Breakdown</h3>
          <p style={{ color: 'var(--text-muted)', fontSize: 'var(--font-size-sm)' }}>
            Per-transaction savings vs. worst-case execution path
          </p>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: 'var(--font-size-xl)', fontWeight: 800, color: 'var(--accent-success)' }}>
            KES {(total_savings_kes || 0).toLocaleString()}
          </div>
          <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--text-muted)' }}>
            Total saved ({(total_savings_pct || 0).toFixed(1)}%)
          </div>
        </div>
      </div>

      {/* Horizontal Bar Chart */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
        {(recommendations || []).map((rec, i) => {
          const widthPct = ((rec.savings_vs_worst || 0) / maxSavings) * 100

          return (
            <div key={i}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 'var(--space-xs)' }}>
                <span style={{ fontSize: 'var(--font-size-sm)', color: 'var(--text-secondary)' }}>
                  {rec.bank_name} — ${(rec.amount_usd || 0).toLocaleString()}
                </span>
                <span style={{ fontSize: 'var(--font-size-sm)', fontFamily: 'var(--font-mono)', color: 'var(--accent-success)', fontWeight: 600 }}>
                  +KES {(rec.savings_vs_worst || 0).toLocaleString()}
                </span>
              </div>
              <div style={{
                height: '8px',
                background: 'var(--bg-elevated)',
                borderRadius: 'var(--radius-full)',
                overflow: 'hidden',
              }}>
                <div style={{
                  height: '100%',
                  width: `${widthPct}%`,
                  background: 'var(--gradient-hero)',
                  borderRadius: 'var(--radius-full)',
                  transition: 'width 1s ease',
                }} />
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
