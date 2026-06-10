import { useState, useRef } from 'react'

// Sample invoices to load when user clicks "Load Sample Data"
const SAMPLE_INVOICES = [
  { id: 'INV-2026-001', supplier_name: 'Guangzhou Auto Parts Co. Ltd', currency: 'USD', amount_usd: 45000, deadline: '2026-06-15', description: 'CKD assembly components - Q3 batch', urgency: 'urgent' },
  { id: 'INV-2026-002', supplier_name: 'Tata Steel International', currency: 'USD', amount_usd: 87500, deadline: '2026-06-18', description: 'Hot-rolled steel coils - 250MT', urgency: 'high' },
  { id: 'INV-2026-003', supplier_name: 'Siemens AG', currency: 'USD', amount_usd: 148000, deadline: '2026-06-25', description: 'PLC automation systems - Factory line 3', urgency: 'medium' },
  { id: 'INV-2026-004', supplier_name: 'Al-Futtaim Trading LLC', currency: 'USD', amount_usd: 23400, deadline: '2026-06-12', description: 'Industrial lubricants & coolants', urgency: 'urgent' },
  { id: 'INV-2026-005', supplier_name: 'SAP SE', currency: 'USD', amount_usd: 35000, deadline: '2026-07-01', description: 'Annual ERP license renewal', urgency: 'low' },
  { id: 'INV-2026-006', supplier_name: 'Shenzhen LED Solutions', currency: 'USD', amount_usd: 12800, deadline: '2026-06-20', description: 'LED industrial lighting panels', urgency: 'medium' },
  { id: 'INV-2026-007', supplier_name: 'Reliance Polymers India', currency: 'USD', amount_usd: 5200, deadline: '2026-06-14', description: 'HDPE polymer granules - 10MT', urgency: 'high' },
  { id: 'INV-2026-008', supplier_name: 'Yokohama Rubber Co.', currency: 'USD', amount_usd: 67000, deadline: '2026-06-30', description: 'Commercial vehicle tyres - Fleet order', urgency: 'medium' },
]

export default function InvoiceUpload({ invoices, onUpload, onNavigateToAnalysis }) {
  const [isDragging, setIsDragging] = useState(false)
  const [uploadStatus, setUploadStatus] = useState(null) // 'success' | 'error' | null
  const fileRef = useRef(null)

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => setIsDragging(false)

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const file = e.dataTransfer.files[0]
    if (file) processFile(file)
  }

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (file) processFile(file)
  }

  const processFile = async (file) => {
    try {
      const text = await file.text()
      const data = JSON.parse(text)
      const invoiceData = data.invoices || data
      const success = await onUpload(invoiceData)
      setUploadStatus(success ? 'success' : 'error')
    } catch {
      setUploadStatus('error')
    }
  }

  const loadSampleData = async () => {
    const success = await onUpload(SAMPLE_INVOICES)
    setUploadStatus(success ? 'success' : 'error')
  }

  const getUrgencyClass = (urgency) => {
    switch (urgency) {
      case 'urgent': return 'high'
      case 'high': return 'high'
      case 'medium': return 'medium'
      default: return 'low'
    }
  }

  const daysUntil = (deadline) => {
    const diff = Math.ceil((new Date(deadline) - new Date()) / (1000 * 60 * 60 * 24))
    return diff
  }

  return (
    <div className="animate-in">
      <div className="page-header">
        <h1>Upload Invoices</h1>
        <p>Import your pending USD-denominated invoices for FX optimization analysis</p>
      </div>

      {/* Upload Zone */}
      <div
        className={`upload-zone ${isDragging ? 'upload-zone--active' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileRef.current?.click()}
        id="invoice-upload-zone"
      >
        <input
          ref={fileRef}
          type="file"
          accept=".json,.csv"
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />
        <div className="upload-zone__icon">📤</div>
        <div className="upload-zone__text">
          Drag & drop your invoice file here, or click to browse
        </div>
        <div className="upload-zone__subtext">
          Accepts JSON files with invoice data (.json)
        </div>
      </div>

      {/* Or Load Sample */}
      <div style={{ textAlign: 'center', margin: 'var(--space-lg) 0' }}>
        <div style={{ color: 'var(--text-muted)', fontSize: 'var(--font-size-sm)', marginBottom: 'var(--space-sm)' }}>
          — or —
        </div>
        <button className="btn btn--secondary" onClick={loadSampleData} id="load-sample-btn">
          📋 Load Sample Kenyan Import Invoices
        </button>
      </div>

      {/* Upload Status */}
      {uploadStatus === 'success' && (
        <div className="glass-card" style={{ borderColor: 'var(--accent-success)', marginTop: 'var(--space-lg)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)', color: 'var(--accent-success)' }}>
            <span>✅</span>
            <strong>{invoices.length} invoices loaded successfully</strong>
          </div>
        </div>
      )}

      {uploadStatus === 'error' && (
        <div className="glass-card" style={{ borderColor: 'var(--accent-danger)', marginTop: 'var(--space-lg)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)', color: 'var(--accent-danger)' }}>
            <span>❌</span>
            <strong>Upload failed — please check the file format</strong>
          </div>
        </div>
      )}

      {/* Invoice Table */}
      {invoices.length > 0 && (
        <>
          <div className="section-divider">
            <div className="section-divider__line" />
            <span className="section-divider__text">Loaded Invoices ({invoices.length})</span>
            <div className="section-divider__line" />
          </div>

          <div className="glass-card glass-card--static" style={{ overflow: 'auto' }}>
            <table className="invoice-table" id="invoice-table">
              <thead>
                <tr>
                  <th>Invoice ID</th>
                  <th>Supplier</th>
                  <th>Amount (USD)</th>
                  <th>Deadline</th>
                  <th>Days Left</th>
                  <th>Priority</th>
                </tr>
              </thead>
              <tbody>
                {invoices.map((inv) => {
                  const days = daysUntil(inv.deadline)
                  return (
                    <tr key={inv.id}>
                      <td className="mono">{inv.id}</td>
                      <td>{inv.supplier_name}</td>
                      <td className="invoice-table__amount">${inv.amount_usd?.toLocaleString()}</td>
                      <td className="invoice-table__deadline">{inv.deadline}</td>
                      <td>
                        <span className={`invoice-table__urgency invoice-table__urgency--${days <= 3 ? 'high' : days <= 7 ? 'medium' : 'low'}`}>
                          {days}d
                        </span>
                      </td>
                      <td>
                        <span className={`invoice-table__urgency invoice-table__urgency--${getUrgencyClass(inv.urgency)}`}>
                          {inv.urgency?.toUpperCase()}
                        </span>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>

          {/* Total + Action */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: 'var(--space-xl)' }}>
            <div>
              <span style={{ color: 'var(--text-muted)', fontSize: 'var(--font-size-sm)' }}>Total USD Exposure: </span>
              <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, fontSize: 'var(--font-size-xl)', color: 'var(--accent-primary)' }}>
                ${invoices.reduce((s, i) => s + (i.amount_usd || 0), 0).toLocaleString()}
              </span>
            </div>
            <button className="btn btn--primary btn--lg" onClick={onNavigateToAnalysis} id="proceed-analysis-btn">
              🧠 Proceed to FX Analysis →
            </button>
          </div>
        </>
      )}
    </div>
  )
}
