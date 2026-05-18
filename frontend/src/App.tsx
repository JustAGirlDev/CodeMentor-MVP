import React from 'react'
import { AppProvider } from './context/AppContext'
import { ErrorBoundary } from './components/ErrorBoundary'
import { PermissionsGate } from './components/PermissionsGate'
import { AssistantView } from './components/AssistantView'
import { SettingsView } from './components/SettingsView'
import { BackendStatus } from './components/BackendStatus'

export default function App() {
  return (
    <AppProvider>
      <ErrorBoundary>
        <PermissionsGate>
          <BackendStatus />
          <div className="app-shell">
            <main className="main">
              <AssistantView />
            </main>
            <aside className="aside">
              <SettingsView />
            </aside>
          </div>
        </PermissionsGate>
      </ErrorBoundary>
    </AppProvider>
  )
}
