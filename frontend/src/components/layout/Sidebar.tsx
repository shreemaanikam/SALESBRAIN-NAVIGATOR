import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  LayoutDashboard, 
  TrendingUp, 
  Package, 
  Users, 
  Map, 
  DollarSign, 
  AlertTriangle, 
  Lightbulb, 
  Sliders, 
  FileText, 
  Database,
  Settings,
  X
} from 'lucide-react';
import { cn } from '@/lib/utils';

const navGroups = [
  {
    title: 'UNDERSTAND',
    items: [
      { name: 'Overview', href: '/dashboard', icon: LayoutDashboard },
      { name: 'Sales', href: '/dashboard/sales', icon: TrendingUp },
      { name: 'Products', href: '/dashboard/products', icon: Package },
      { name: 'Customers', href: '/dashboard/customers', icon: Users },
      { name: 'Geography', href: '/dashboard/geography', icon: Map },
    ]
  },
  {
    title: 'DECIDE',
    items: [
      { name: 'Profitability', href: '/dashboard/profitability', icon: DollarSign },
      { name: 'Risk Center', href: '/dashboard/risk', icon: AlertTriangle },
      { name: 'AI Insights', href: '/dashboard/ai-insights', icon: Lightbulb },
      { name: 'What-If Simulator', href: '/dashboard/what-if', icon: Sliders },
    ]
  },
  {
    title: 'MANAGE',
    items: [
      { name: 'Reports', href: '/dashboard/reports', icon: FileText },
      { name: 'Data Explorer', href: '/dashboard/data', icon: Database },
      { name: 'Settings', href: '/dashboard/settings', icon: Settings },
    ]
  }
];

export function Sidebar({ isMobile = false, isOpen = true, onClose }: { isMobile?: boolean, isOpen?: boolean, onClose?: () => void }) {
  const pathname = usePathname();

  const sidebarContent = (
    <>
      <div className="p-6 flex items-center justify-between">
        <Link href="/">
          <h2 className="text-xl font-bold tracking-tight text-slate-900 dark:text-white hover:text-blue-600 transition-colors">
            SalesBrain
            <span className="text-blue-600 block text-sm font-medium">Navigator</span>
          </h2>
        </Link>
        {isMobile && (
          <button onClick={onClose} className="p-2 -mr-2 text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white">
            <X className="w-5 h-5" />
          </button>
        )}
      </div>
      
      <div className="flex-1 overflow-y-auto px-4 pb-6 space-y-6">
        {navGroups.map((group) => (
          <div key={group.title}>
            <h3 className="px-3 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-2">
              {group.title}
            </h3>
            <div className="space-y-1">
              {group.items.map((item) => {
                const isActive = pathname === item.href || (item.href !== '/dashboard' && pathname.startsWith(item.href));
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    onClick={isMobile ? onClose : undefined}
                    className={cn(
                      "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                      isActive 
                        ? "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400" 
                        : "text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-white"
                    )}
                  >
                    <item.icon className={cn("w-4 h-4", isActive ? "text-blue-600 dark:text-blue-400" : "text-slate-400 dark:text-slate-500")} />
                    {item.name}
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </>
  );

  if (isMobile) {
    return (
      <div className={cn("fixed inset-0 z-50 flex", isOpen ? "" : "pointer-events-none")}>
        <div 
          className={cn("fixed inset-0 bg-slate-900/50 backdrop-blur-sm transition-opacity", isOpen ? "opacity-100" : "opacity-0")}
          onClick={onClose}
        />
        <div className={cn("relative flex w-64 flex-col bg-white dark:bg-slate-950 transition-transform duration-300 ease-in-out", isOpen ? "translate-x-0" : "-translate-x-full")}>
          {sidebarContent}
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col w-64 border-r border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950 h-screen sticky top-0 hidden md:flex">
      {sidebarContent}
    </div>
  );
}
