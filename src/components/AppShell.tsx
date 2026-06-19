import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import TopBar from './TopBar'

export default function AppShell() {
  return (
    <div className="relative flex min-h-screen bg-ink-950">
      {/* Ambient glow so the dark app reads as part of the same world as the site */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="aurora -left-40 -top-40 h-[32rem] w-[32rem] opacity-25" style={{ background: 'radial-gradient(circle, #8b5cf6, transparent 70%)' }} />
        <div className="aurora bottom-0 right-0 h-[28rem] w-[28rem] opacity-20" style={{ background: 'radial-gradient(circle, #22d3ee, transparent 70%)' }} />
      </div>
      <Sidebar />
      <div className="relative z-10 flex min-w-0 flex-1 flex-col">
        <TopBar />
        <main className="flex-1 overflow-x-hidden p-4 sm:p-6">
          <div className="mx-auto max-w-7xl">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  )
}
