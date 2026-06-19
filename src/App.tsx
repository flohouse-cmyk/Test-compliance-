import { Navigate, Route, Routes } from 'react-router-dom'
import Landing from './views/Landing'
import AppShell from './components/AppShell'
import LeadershipView from './views/LeadershipView'
import TeamLeadView from './views/TeamLeadView'
import DevView from './views/DevView'
import InsightsView from './views/InsightsView'
import FrameworksView from './views/FrameworksView'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/app" element={<AppShell />}>
        <Route index element={<Navigate to="leadership" replace />} />
        <Route path="leadership" element={<LeadershipView />} />
        <Route path="team" element={<TeamLeadView />} />
        <Route path="delivery" element={<DevView />} />
        <Route path="insights" element={<InsightsView />} />
        <Route path="frameworks" element={<FrameworksView />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
