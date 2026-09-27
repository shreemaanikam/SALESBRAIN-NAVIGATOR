/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React from 'react';
import { usePathname } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';
import { Sidebar } from '@/components/layout/Sidebar';
import { Topbar } from '@/components/layout/Topbar';
import { useUIStore } from '@/store/store';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isMobileMenuOpen, toggleMobileMenu, setMobileMenuOpen } = useUIStore();
  const pathname = usePathname();
  const isRootDashboard = pathname === '/dashboard';

  return (
    <div className="flex h-screen overflow-hidden bg-slate-50 dark:bg-slate-900 transition-colors">
      {/* Desktop Sidebar */}
      <Sidebar />
      
      {/* Mobile Sidebar */}
      <div className="md:hidden">
        <Sidebar isMobile isOpen={isMobileMenuOpen} onClose={() => setMobileMenuOpen(false)} />
      </div>
      
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Topbar onMenuClick={toggleMobileMenu} />
        
        <main className="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8">
          <div className="mx-auto max-w-7xl">
            {!isRootDashboard && !pathname.includes('/products/') && (
              <div className="mb-6">
                <Link href="/dashboard" className="inline-flex items-center gap-2 text-sm text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-white transition-colors">
                  <ArrowLeft className="w-4 h-4" /> Back to Dashboard
                </Link>
              </div>
            )}
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
