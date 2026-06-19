import { Navigate, Route, Routes } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import TopBar from './components/TopBar'
import LeadershipView from './views/LeadershipView'
import TeamLeadView from './views/TeamLeadView'
import DevView from './views/DevView'
import InsightsView from './views/InsightsView'
import FrameworksView from './views/FrameworksView'

export default function App() {
  return (
    <div className="flex min-h-screen bg-ink-950">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <TopBar />
        <main className="grain flex-1 overflow-x-hidden p-4 sm:p-6">
          <div className="mx-auto max-w-7xl">
            <Routes>
              <Route path="/" element={<Navigate to="/leadership" replace />} />
              <Route path="/leadership" element={<LeadershipView />} />
              <Route path="/team" element={<TeamLeadView />} />
              <Route path="/delivery" element={<DevView />} />
              <Route path="/insights" element={<InsightsView />} />
              <Route path="/frameworks" element={<FrameworksView />} />
              <Route path="*" element={<Navigate to="/leadership" replace />} />
            </Routes>
          </div>
        </main>
      </div>
    </div>
  )
}
