import { useState, useCallback } from 'react'
import Navbar from './components/Navbar'
import Dashboard from './components/Dashboard'
import InvoiceUpload from './components/InvoiceUpload'
import AnalysisView from './components/AnalysisView'
import ReportsView from './components/ReportsView'

const API_BASE = '/api'

export default function App() {
  const [activeView, setActiveView] = useState('dashboard')
  const [invoices, setInvoices] = useState([])
  const [rates, setRates] = useState([])
  const [analysisReport, setAnalysisReport] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [reports, setReports] = useState([])

  /* ---- Data Fetching ---- */
  const fetchRates = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/rates`)
      if (res.ok) {
        const data = await res.json()
        setRates(data.rates || data)
      }
    } catch (err) {
      console.error('Failed to fetch rates:', err)
    }
  }, [])

  const uploadInvoices = useCallback(async (invoiceData) => {
    try {
      const res = await fetch(`${API_BASE}/invoices`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ invoices: invoiceData }),
      })
      if (res.ok) {
        const data = await res.json()
        setInvoices(data.invoices || invoiceData)
        return true
      }
    } catch (err) {
      console.error('Failed to upload invoices:', err)
    }
    return false
  }, [])

  const runAnalysis = useCallback(async () => {
    setIsAnalyzing(true)
    setAnalysisReport(null)
    try {
      const res = await fetch(`${API_BASE}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ invoice_ids: invoices.map(inv => inv.id) }),
      })
      if (res.ok) {
        const data = await res.json()
        setAnalysisReport(data)
        setReports(prev => [data, ...prev])
      }
    } catch (err) {
      console.error('Analysis failed:', err)
    } finally {
      setIsAnalyzing(false)
    }
  }, [invoices])

  /* ---- Render Views ---- */
  const renderView = () => {
    switch (activeView) {
      case 'dashboard':
        return (
          <Dashboard
            rates={rates}
            invoices={invoices}
            analysisReport={analysisReport}
            fetchRates={fetchRates}
          />
        )
      case 'upload':
        return (
          <InvoiceUpload
            invoices={invoices}
            onUpload={uploadInvoices}
            onNavigateToAnalysis={() => setActiveView('analysis')}
          />
        )
      case 'analysis':
        return (
          <AnalysisView
            invoices={invoices}
            rates={rates}
            report={analysisReport}
            isAnalyzing={isAnalyzing}
            onRunAnalysis={runAnalysis}
            fetchRates={fetchRates}
          />
        )
      case 'reports':
        return <ReportsView reports={reports} />
      default:
        return null
    }
  }

  return (
    <div className="app-layout">
      <Navbar activeView={activeView} onNavigate={setActiveView} />
      <main className="main-content">
        {renderView()}
      </main>
    </div>
  )
}
