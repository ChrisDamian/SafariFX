export default function ReportsView({ reports }) {
  if (!reports || reports.length === 0) {
    return (
      <div className="animate-in">
        <div className="page-header">
          <h1>Analysis Reports</h1>
          <p>Historical audit trail of all FX optimization decisions</p>
        </div>
        <div className="glass-card glass-card--static" style={{ textAlign: 'center', padding: 'var(--space-3xl)' }}>
          <div style={{ fontSize: '3rem', marginBottom: 'var(--space-md)', opacity: 0.5 }}>📋</div>
          <h3 style={{ color: 'var(--text-secondary)', marginBottom: 'var(--space-sm)' }}>No Reports Yet</h3>
          <p style={{ color: 'var(--text-muted)', fontSize: 'var(--font-size-sm)' }}>
            Run an FX analysis from the Analysis tab to generate your first report.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="animate-in">
      <div className="page-header">
        <h1>Analysis Reports</h1>
        <p>Historical audit trail — {reports.length} report{reports.length !== 1 ? 's' : ''} generated</p>
      </div>

      <div className="stagger-children">
        {reports.map((report, i) => (
          <div className="glass-card" key={report.id || i} style={{ marginBottom: 'var(--space-lg)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--space-md)' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)' }}>
                  <span className="status-badge status-badge--success">Complete</span>
                  <span className="mono" style={{ fontSize: 'var(--font-size-xs)', color: 'var(--text-muted)' }}>
                    {report.id}
                  </span>
                </div>
                <div style={{ color: 'var(--text-muted)', fontSize: 'var(--font-size-xs)', marginTop: 'var(--space-xs)' }}>
                  Generated: {report.timestamp ? new Date(report.timestamp).toLocaleString() : 'N/A'}
                </div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: 'var(--font-size-lg)', fontWeight: 700, color: 'var(--accent-success)' }}>
                  KES {(report.total_savings_kes || 0).toLocaleString()}
                </div>
                <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--text-muted)' }}>
                  saved ({(report.total_savings_pct || 0).toFixed(1)}%)
                </div>
              </div>
            </div>

            {/* Summary Stats */}
            <div style={{ display: 'flex', gap: 'var(--space-xl)', borderTop: '1px solid var(--glass-border)', paddingTop: 'var(--space-md)' }}>
              <div>
                <span style={{ color: 'var(--text-muted)', fontSize: 'var(--font-size-xs)' }}>Invoices: </span>
                <span className="mono" style={{ color: 'var(--text-primary)', fontWeight: 600 }}>
                  {(report.invoices || []).length}
                </span>
              </div>
              <div>
                <span style={{ color: 'var(--text-muted)', fontSize: 'var(--font-size-xs)' }}>Recommendations: </span>
                <span className="mono" style={{ color: 'var(--text-primary)', fontWeight: 600 }}>
                  {(report.recommendations || []).length}
                </span>
              </div>
              <div>
                <span style={{ color: 'var(--text-muted)', fontSize: 'var(--font-size-xs)' }}>Reasoning Steps: </span>
                <span className="mono" style={{ color: 'var(--text-primary)', fontWeight: 600 }}>
                  {(report.reasoning_steps || []).length}
                </span>
              </div>
              <div>
                <span style={{ color: 'var(--text-muted)', fontSize: 'var(--font-size-xs)' }}>Banks Compared: </span>
                <span className="mono" style={{ color: 'var(--text-primary)', fontWeight: 600 }}>
                  {(report.rates_snapshot || []).length}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
