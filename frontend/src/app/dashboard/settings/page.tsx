/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Moon, Sun, Monitor, Bell, Database } from 'lucide-react';
import { useTheme } from 'next-themes';
import { getHealth } from '@/services/api';

export default function SettingsPage() {
  const { theme, setTheme } = useTheme();
  const [apiStatus, setApiStatus] = useState<'Checking...' | 'Online (Live API)' | 'Offline (Mock Mode)'>('Checking...');
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);

  useEffect(() => {
    getHealth()
      .then(res => {
        if (res && res.status === 'ok') setApiStatus('Online (Live API)');
        else setApiStatus('Offline (Mock Mode)');
      })
      .catch(() => setApiStatus('Offline (Mock Mode)'));
  }, []);

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">Settings</h1>
        <p className="text-slate-500 dark:text-slate-400">Manage your workspace preferences and application settings.</p>
        <p className="text-xs text-slate-400 mt-2 italic">Note: These settings are local to your browser session.</p>
      </div>

      <Card className="dark:bg-slate-900 dark:border-slate-800">
        <CardHeader>
          <div className="flex items-center gap-2">
            <Monitor className="w-5 h-5 text-slate-500" />
            <CardTitle className="dark:text-white">Appearance</CardTitle>
          </div>
          <CardDescription className="dark:text-slate-400">Customize the look and feel of SalesBrain Navigator.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-4">
            <button 
              onClick={() => setTheme('light')}
              className={`flex flex-col items-center justify-center p-4 rounded-lg border-2 transition-all ${
                theme === 'light' ? 'border-blue-600 bg-blue-50 dark:bg-blue-900/20' : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600'
              }`}
            >
              <Sun className={`w-8 h-8 mb-2 ${theme === 'light' ? 'text-blue-600' : 'text-slate-400'}`} />
              <span className="text-sm font-medium dark:text-slate-300">Light</span>
            </button>
            <button 
              onClick={() => setTheme('dark')}
              className={`flex flex-col items-center justify-center p-4 rounded-lg border-2 transition-all ${
                theme === 'dark' ? 'border-blue-600 bg-blue-50 dark:bg-blue-900/20' : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600'
              }`}
            >
              <Moon className={`w-8 h-8 mb-2 ${theme === 'dark' ? 'text-blue-600' : 'text-slate-400'}`} />
              <span className="text-sm font-medium dark:text-slate-300">Dark</span>
            </button>
            <button 
              onClick={() => setTheme('system')}
              className={`flex flex-col items-center justify-center p-4 rounded-lg border-2 transition-all ${
                theme === 'system' ? 'border-blue-600 bg-blue-50 dark:bg-blue-900/20' : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600'
              }`}
            >
              <Monitor className={`w-8 h-8 mb-2 ${theme === 'system' ? 'text-blue-600' : 'text-slate-400'}`} />
              <span className="text-sm font-medium dark:text-slate-300">System</span>
            </button>
          </div>
        </CardContent>
      </Card>

      <Card className="dark:bg-slate-900 dark:border-slate-800">
        <CardHeader>
          <div className="flex items-center gap-2">
            <Database className="w-5 h-5 text-slate-500" />
            <CardTitle className="dark:text-white">Workspace Data</CardTitle>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex justify-between items-center py-3 border-b border-slate-100 dark:border-slate-800">
            <div>
              <p className="font-medium text-slate-900 dark:text-white">Connected Dataset</p>
              <p className="text-sm text-slate-500 dark:text-slate-400">Cleaned_SuperStore.csv</p>
            </div>
            <span className="px-3 py-1 bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400 rounded-full text-xs font-semibold">Active</span>
          </div>
          <div className="flex justify-between items-center py-3 border-b border-slate-100 dark:border-slate-800">
            <div>
              <p className="font-medium text-slate-900 dark:text-white">Machine Learning API</p>
              <p className="text-sm text-slate-500 dark:text-slate-400">Status of the prediction backend</p>
            </div>
            <span className={`px-3 py-1 rounded-full text-xs font-semibold ${apiStatus === 'Online (Live API)' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400' : 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400'}`}>
              {apiStatus}
            </span>
          </div>
        </CardContent>
      </Card>

      <Card className="dark:bg-slate-900 dark:border-slate-800">
        <CardHeader>
          <div className="flex items-center gap-2">
            <Bell className="w-5 h-5 text-slate-500" />
            <CardTitle className="dark:text-white">Notifications</CardTitle>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium text-slate-900 dark:text-white">Risk Alerts</p>
              <p className="text-sm text-slate-500 dark:text-slate-400">Receive alerts for high-risk outliers (statistical method).</p>
            </div>
            <div 
              className={`w-11 h-6 rounded-full relative cursor-pointer transition-colors ${notificationsEnabled ? 'bg-blue-600' : 'bg-slate-200 dark:bg-slate-700'}`}
              onClick={() => setNotificationsEnabled(!notificationsEnabled)}
            >
              <div className={`w-4 h-4 bg-white rounded-full absolute top-1 transition-all ${notificationsEnabled ? 'right-1' : 'left-1'}`}></div>
            </div>
          </div>
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium text-slate-900 dark:text-white">Weekly Digest</p>
              <p className="text-sm text-slate-500 dark:text-slate-400">Automated email summarizing weekly sales.</p>
            </div>
            <div className="w-11 h-6 bg-slate-200 dark:bg-slate-700 rounded-full relative cursor-not-allowed" title="Coming soon">
              <div className="w-4 h-4 bg-white rounded-full absolute top-1 left-1"></div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
