import { NavLink, Outlet } from 'react-router-dom';
import { BarChart3, Bot, Inbox, LayoutDashboard, Search, Settings, UserRound, MessagesSquare } from 'lucide-react';

const nav = [
  ['Dashboard', '/dashboard', LayoutDashboard],
  ['Inbox', '/inbox', Inbox],
  ['AI Analysis', '/ai', Bot],
  ['Knowledge', '/knowledge', Search],
  ['Analytics', '/analytics', BarChart3],
  ['Customers', '/customers/1', UserRound],
  ['Settings', '/settings', Settings],
];

export default function AppShell() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-slate-200 bg-white px-4 py-5 lg:block">
        <div className="mb-8 flex items-center gap-3 px-2">
          <div className="grid h-9 w-9 place-items-center rounded bg-teal-600 text-white"><MessagesSquare size={18} /></div>
          <div>
            <p className="text-sm font-semibold">SenAI CRM</p>
            <p className="text-xs text-slate-500">AI operations console</p>
          </div>
        </div>
        <nav className="space-y-1">
          {nav.map(([label, path, Icon]) => (
            <NavLink key={path} to={path} className={({ isActive }) => `flex items-center gap-3 rounded px-3 py-2 text-sm ${isActive ? 'bg-teal-50 text-teal-700' : 'text-slate-600 hover:bg-slate-100'}`}>
              <Icon size={17} />
              {label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="lg:pl-64">
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
