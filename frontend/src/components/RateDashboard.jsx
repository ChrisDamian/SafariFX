/**
 * Sparkline — A tiny inline SVG chart showing 7-day rate trend
 */
function Sparkline({ data, color = 'var(--accent-primary)' }) {
  if (!data || data.length < 2) return null

  const min = Math.min(...data)
  const max = Math.max(...data)
  const range = max - min || 1
  const h = 40
  const w = 120
  const padding = 2

  const points = data.map((val, i) => {
    const x = padding + (i / (data.length - 1)) * (w - 2 * padding)
    const y = h - padding - ((val - min) / range) * (h - 2 * padding)
    return `${x},${y}`
  })

  const linePath = `M ${points.join(' L ')}`
  const areaPath = `${linePath} L ${w - padding},${h} L ${padding},${h} Z`

  const gradientId = `sg-${Math.random().toString(36).slice(2, 8)}`

  return (
    <div className="rate-card__sparkline">
      <svg viewBox={`0 0 ${w} ${h}`} preserveAspectRatio="none">
        <defs>
          <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={color} stopOpacity="0.3" />
            <stop offset="100%" stopColor={color} stopOpacity="0" />
          </linearGradient>
        </defs>
        <path d={areaPath} fill={`url(#${gradientId})`} />
        <path d={linePath} fill="none" stroke={color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </div>
  )
}

/**
 * RateDashboard — Grid of bank rate cards with sparklines
 */
export default function RateDashboard({ rates }) {
  if (!rates || rates.length === 0) {
    return (
      <div className="glass-card glass-card--static" style={{ textAlign: 'center', padding: 'var(--space-2xl)' }}>
        <div style={{ fontSize: '2rem', marginBottom: 'var(--space-md)', opacity: 0.5 }}>📡</div>
        <p style={{ color: 'var(--text-muted)' }}>Loading interbank rates...</p>
      </div>
    )
  }

  const getSpreadClass = (spread) => {
    if (spread <= 1.0) return 'tight'
    if (spread <= 1.8) return 'medium'
    return 'wide'
  }

  const getSpreadLabel = (spread) => {
    if (spread <= 1.0) return 'Tight'
    if (spread <= 1.8) return 'Standard'
    return 'Wide'
  }

  return (
    <div className="grid-5 stagger-children">
      {rates.map((bank) => {
        const spread = bank.sell_rate - bank.buy_rate
        const spreadClass = getSpreadClass(spread)

        return (
          <div className="rate-card" key={bank.bank_code} id={`rate-${bank.bank_code}`}>
            <div className="rate-card__bank">{bank.bank_name}</div>
            <div className="rate-card__code">{bank.bank_code}</div>

            <div style={{ display: 'flex', gap: 'var(--space-lg)' }}>
              <div>
                <div className="rate-card__rate">{bank.buy_rate?.toFixed(2)}</div>
                <div className="rate-card__label">Buy Rate</div>
              </div>
              <div>
                <div className="rate-card__rate" style={{ color: 'var(--text-secondary)', fontSize: 'var(--font-size-lg)' }}>
                  {bank.sell_rate?.toFixed(2)}
                </div>
                <div className="rate-card__label">Sell Rate</div>
              </div>
            </div>

            <div className={`rate-card__spread rate-card__spread--${spreadClass}`}>
              <span>↔</span> {spread.toFixed(2)} KES — {getSpreadLabel(spread)}
            </div>

            <div className="rate-card__liquidity">
              <span className={`rate-card__liquidity-dot rate-card__liquidity-dot--${bank.liquidity_indicator || 'medium'}`} />
              {(bank.liquidity_indicator || 'medium').charAt(0).toUpperCase() + (bank.liquidity_indicator || 'medium').slice(1)} Liquidity
            </div>

            <Sparkline data={bank.trend_7d} />
          </div>
        )
      })}
    </div>
  )
}
