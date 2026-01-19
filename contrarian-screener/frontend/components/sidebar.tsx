import Link from "next/link";
import { LayoutDashboard, Telescope, Eye, Settings } from "lucide-react";

export function Sidebar() {
  return (
    <div className="h-screen w-64 bg-slate-950 border-r border-slate-800 text-slate-300 p-4 fixed left-0 top-0 flex flex-col">
      <div className="flex items-center gap-2 mb-8 px-2">
        <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center text-slate-950 font-bold">
          C
        </div>
        <span className="font-bold text-xl text-white tracking-tight">Contrarian</span>
      </div>

      <nav className="flex-1 space-y-1">
        <NavLink href="/" icon={<LayoutDashboard size={20} />} label="Dashboard" />
        <NavLink href="/screen" icon={<Telescope size={20} />} label="Screener" />
        <NavLink href="/watchlist" icon={<Eye size={20} />} label="Watchlist" />
      </nav>

      <div className="mt-auto pt-4 border-t border-slate-800">
        <NavLink href="/settings" icon={<Settings size={20} />} label="Settings" />
      </div>
    </div>
  );
}

function NavLink({ href, icon, label }: { href: string; icon: React.ReactNode; label: string }) {
  return (
    <Link 
      href={href} 
      className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-900 hover:text-white transition-colors"
    >
      {icon}
      <span>{label}</span>
    </Link>
  );
}
