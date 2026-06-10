export default function ReasoningTrace({ steps, isActive }) {
  if (!steps || steps.length === 0) return null

  return (
    <div className="reasoning-trace" id="reasoning-trace">
      {steps.map((step) => {
        const isComplete = step.confidence && step.confidence > 0
        const isCurrentlyActive = isActive && !isComplete

        return (
          <div
            key={step.step_number}
            className={`reasoning-step ${isComplete ? 'reasoning-step--complete' : ''} ${isCurrentlyActive ? 'reasoning-step--active' : ''}`}
          >
            {/* Step Indicator */}
            <div className="reasoning-step__indicator">
              {isComplete ? '✓' : step.step_number}
            </div>

            {/* Step Content */}
            <div className="reasoning-step__content">
              <div className="reasoning-step__title">
                Step {step.step_number}: {step.title}
              </div>
              <div className="reasoning-step__description">
                {step.description}
              </div>

              {/* Input Summary */}
              {step.input_summary && (
                <div style={{
                  padding: 'var(--space-sm) var(--space-md)',
                  background: 'var(--bg-input)',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: 'var(--font-size-xs)',
                  fontFamily: 'var(--font-mono)',
                  color: 'var(--text-secondary)',
                  marginBottom: 'var(--space-sm)',
                  lineHeight: 1.6,
                }}>
                  {step.input_summary}
                </div>
              )}

              {/* Conclusion */}
              {step.conclusion && (
                <div style={{
                  padding: 'var(--space-md)',
                  background: 'hsla(170, 80%, 45%, 0.05)',
                  border: '1px solid hsla(170, 80%, 45%, 0.12)',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: 'var(--font-size-sm)',
                  color: 'var(--text-primary)',
                  lineHeight: 1.6,
                }}>
                  <span style={{ color: 'var(--accent-primary)', fontWeight: 600 }}>→ </span>
                  {step.conclusion}
                </div>
              )}

              {/* IQ Citation */}
              {step.iq_citation && (
                <div className="reasoning-step__citation">
                  <span className="reasoning-step__citation-icon">📎</span>
                  <div>
                    <div style={{ fontWeight: 600, marginBottom: '2px' }}>
                      {step.iq_source || 'Foundry IQ Knowledge Base'}
                    </div>
                    <div style={{ opacity: 0.8 }}>{step.iq_citation}</div>
                  </div>
                </div>
              )}

              {/* Confidence Bar */}
              {step.confidence > 0 && (
                <div className="reasoning-step__confidence">
                  <div className="reasoning-step__confidence-bar">
                    <div
                      className="reasoning-step__confidence-fill"
                      style={{ width: `${step.confidence * 100}%` }}
                    />
                  </div>
                  <span className="reasoning-step__confidence-label">
                    {(step.confidence * 100).toFixed(0)}% confidence
                  </span>
                </div>
              )}

              {/* Duration */}
              {step.duration_ms > 0 && (
                <div style={{
                  marginTop: 'var(--space-sm)',
                  fontSize: 'var(--font-size-xs)',
                  color: 'var(--text-muted)',
                  fontFamily: 'var(--font-mono)',
                }}>
                  ⏱ {step.duration_ms}ms
                </div>
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}
