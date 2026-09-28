"use client";
import React, { createContext, useContext, useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';

interface User {
  uid: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
  login: () => {},
  logout: () => {},
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    // Check local storage for dummy token
    const token = localStorage.getItem('salesbrain_token');
    if (token) {
      setUser({ uid: token, email: 'demo@salesbrain.ai' });
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    if (!loading && !user && pathname?.startsWith('/dashboard')) {
      router.push('/login');
    }
  }, [user, loading, pathname, router]);

  const login = (email: string) => {
    // For local auth mode, the token is simply the user ID.
    // In a real Firebase setup, this would call signInWithEmailAndPassword
    const dummyToken = email.split('@')[0] + "_local_id";
    localStorage.setItem('salesbrain_token', dummyToken);
    setUser({ uid: dummyToken, email });
    router.push('/dashboard');
  };

  const logout = () => {
    localStorage.removeItem('salesbrain_token');
    setUser(null);
    router.push('/login');
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
