import React from 'react';
import { Search, Bell, Menu, Calendar, Filter, Moon, Sun } from 'lucide-react';
import { useFilterStore } from '@/store/store';
import { useTheme } from 'next-themes';

export function Topbar({ onMenuClick }: { onMenuClick?: () => void }) {
  const { searchQuery, setSearchQuery } = useFilterStore();
  const { theme, setTheme } = useTheme();

  return (
    <header className="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 h-16 flex items-center justify-between px-4 sticky top-0 z-10 transition-colors">
      <div className="flex items-center gap-4 flex-1">
        <button 
          className="md:hidden p-2 -ml-2 text-slate-500 hover:text-slate-900 dark:hover:text-white rounded-md hover:bg-slate-50 dark:hover:bg-slate-800"
          onClick={onMenuClick}
        >
          <Menu className="w-5 h-5" />
        </button>
        
        <div className="hidden md:flex items-center gap-2 px-3 py-1.5 bg-slate-100 dark:bg-slate-800 rounded-md border border-slate-200 dark:border-slate-700 focus-within:border-blue-500 focus-within:bg-white dark:focus-within:bg-slate-900 transition-colors max-w-md w-full">
          <Search className="w-4 h-4 text-slate-400" />
          <input 
            type="text" 
            placeholder="Search products, categories, or regions..." 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="bg-transparent border-none outline-none text-sm w-full placeholder:text-slate-500 dark:text-white"
          />
        </div>
      </div>

      <div className="flex items-center gap-2 md:gap-4">
        <div className="hidden lg:flex items-center gap-4 mr-4">
          <button className="flex items-center gap-2 text-sm text-slate-400 dark:text-slate-600 bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-800 px-3 py-1.5 rounded-md cursor-not-allowed" title="Coming soon">
            <Calendar className="w-4 h-4" />
            <span>Last 12 Months</span>
          </button>
          <button className="flex items-center gap-2 text-sm text-slate-400 dark:text-slate-600 bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-800 px-3 py-1.5 rounded-md cursor-not-allowed" title="Coming soon">
            <Filter className="w-4 h-4" />
            <span>Filters</span>
          </button>
        </div>

        <button 
          onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
          className="p-2 text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white hover:bg-slate-50 dark:hover:bg-slate-800 rounded-full transition-colors"
          title="Toggle theme"
        >
          {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
        </button>

        <button className="p-2 text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-full relative transition-colors cursor-not-allowed" title="Notifications (Coming soon)">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-slate-300 dark:bg-slate-600 rounded-full border-2 border-white dark:border-slate-900"></span>
        </button>
        
        <div className="h-8 w-8 bg-slate-200 dark:bg-slate-700 rounded-full flex items-center justify-center text-slate-500 dark:text-slate-400 cursor-not-allowed shrink-0" title="Profile (Coming soon)">
          <span className="text-sm font-semibold">SA</span>
        </div>
      </div>
    </header>
  );
}
