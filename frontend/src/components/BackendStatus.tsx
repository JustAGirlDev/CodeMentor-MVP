import React, { useState, useEffect } from 'react'

export function BackendStatus() {
  const [status, setStatus] = useState<'connecting' | 'online' | 'offline'>('connecting')
  const [version, setVersion] = useState('')

  useEffect(() => {
    fetch('/api/health')
      .then(r => r.json())
      .then(d => {
        setStatus('online')
        setVersion(d.version || 'unknown')
      })
      .catch(() => setStatus('offline'))
  }, [])

  const color = status === 'online' ? '#00ff88' : status === 'connecting' ? '#ffd93d' : '#ff4444'
  
  return (
    <div style={{ 
      position: 'fixed', 
      top: 10, 
      right: 10, 
      padding: '8px 16px',
      background: '#1a1a2e',
      border: `2px solid ${color}`,
      borderRadius: 8,
      color,
      fontFamily: 'monospace',
      fontSize: 12,
      zIndex: 9999
    }}>
      ● {status.toUpperCase()} {version && `| v${version}`}
    </div>
  )
}
