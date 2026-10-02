"use client";

import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/Card';
import { useAuth } from '@/contexts/AuthContext';
import { Brain, ArrowRight } from 'lucide-react';

export default function LoginPage() {
  const [email, setEmail] = useState('demo@salesbrain.ai');
  const [password, setPassword] = useState('password123');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { login, authMode } = useAuth();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim()) return;
    
    setIsSubmitting(true);
    setError('');
    try {
      await login(email, password);
    } catch (err: any) { // eslint-disable-line @typescript-eslint/no-explicit-any
      console.error('Login failed:', err);
      // Give a clean error message, avoiding leaking internal details
      if (err.code === 'auth/invalid-credential' || err.code === 'auth/user-not-found' || err.code === 'auth/wrong-password') {
        setError('Invalid email or password.');
      } else if (err.code === 'auth/too-many-requests') {
        setError('Account temporarily disabled due to many failed login attempts. Try again later.');
      } else {
        setError(err.message || 'An error occurred during sign in.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-900 p-4">
      <div className="w-full max-w-md">
        <div className="flex items-center justify-center gap-2 mb-8 text-blue-600 dark:text-blue-500">
          <Brain className="h-10 w-10" />
          <span className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">SalesBrain</span>
        </div>
        
        <Card className="border-slate-200 dark:border-slate-800 shadow-lg">
          <CardHeader className="space-y-1">
            <CardTitle className="text-2xl text-center">Welcome back</CardTitle>
            <CardDescription className="text-center">
              Sign in to your isolated workspace
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleLogin} className="space-y-4">
              {error && (
                <div className="bg-red-50 text-red-600 text-sm p-3 rounded-md border border-red-200">
                  {error}
                </div>
              )}
              <div className="space-y-2">
                <label htmlFor="email" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 dark:text-slate-300">
                  Email
                </label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="flex h-10 w-full rounded-md border border-slate-300 bg-transparent px-3 py-2 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-700 dark:text-slate-50 dark:focus:ring-blue-500"
                  placeholder="name@example.com"
                  required
                  disabled={isSubmitting}
                />
              </div>
              
              {authMode === 'firebase' && (
                <div className="space-y-2">
                  <label htmlFor="password" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 dark:text-slate-300">
                    Password
                  </label>
                  <input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="flex h-10 w-full rounded-md border border-slate-300 bg-transparent px-3 py-2 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-700 dark:text-slate-50 dark:focus:ring-blue-500"
                    required
                    disabled={isSubmitting}
                  />
                </div>
              )}

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 disabled:opacity-50 disabled:pointer-events-none bg-blue-600 text-white hover:bg-blue-700 h-10 py-2 px-4"
              >
                {isSubmitting ? 'Signing in...' : 'Sign In'}
                {!isSubmitting && <ArrowRight className="ml-2 h-4 w-4" />}
              </button>
            </form>
          </CardContent>
          <div className="flex flex-col text-sm text-slate-500 dark:text-slate-400 text-center space-y-2 p-6 pt-0">
            <p>Don&apos;t have an account? <span className="text-blue-600 hover:underline cursor-pointer">Sign up</span></p>
            <p className="text-xs">
              Authentication is currently running in <span className="font-semibold">{authMode}</span> mode.
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
}
