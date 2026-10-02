"use client";
import React, { createContext, useContext, useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { auth } from '@/lib/firebase';
import { onAuthStateChanged, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut, signInWithPopup, GoogleAuthProvider } from 'firebase/auth';

interface User {
  uid: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password?: string) => Promise<void>;
  signup: (email: string, password?: string) => Promise<void>;
  loginWithGoogle: () => Promise<void>;
  logout: () => Promise<void>;
  authMode: 'local' | 'firebase';
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
  login: async () => {},
  signup: async () => {},
  loginWithGoogle: async () => {},
  logout: async () => {},
  authMode: 'local',
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  const authMode = (process.env.NEXT_PUBLIC_AUTH_MODE || 'local') as 'local' | 'firebase';

  useEffect(() => {
    if (authMode === 'local') {
      const token = localStorage.getItem('salesbrain_token');
      if (token) {
        setUser({ uid: token, email: 'demo@salesbrain.ai' });
      }
      setLoading(false);
    } else {
      if (!auth) {
        console.error("Firebase Auth is not initialized. Check your environment variables.");
        setLoading(false);
        return;
      }
      const unsubscribe = onAuthStateChanged(auth, (firebaseUser) => {
        if (firebaseUser) {
          setUser({ uid: firebaseUser.uid, email: firebaseUser.email || '' });
        } else {
          setUser(null);
        }
        setLoading(false);
      });
      return () => unsubscribe();
    }
  }, [authMode]);

  useEffect(() => {
    if (!loading && !user && pathname?.startsWith('/dashboard')) {
      router.push('/login');
    }
  }, [user, loading, pathname, router]);

  const login = async (email: string, password?: string) => {
    if (authMode === 'local') {
      const dummyToken = email.split('@')[0] + "_local_id";
      localStorage.setItem('salesbrain_token', dummyToken);
      setUser({ uid: dummyToken, email });
      router.push('/dashboard');
    } else {
      if (!auth) throw new Error('Firebase Auth is not initialized. Please check your configuration.');
      if (!password) throw new Error('Password is required in Firebase mode');
      await signInWithEmailAndPassword(auth, email, password);
      router.push('/dashboard');
    }
  };

  const signup = async (email: string, password?: string) => {
    if (authMode === 'local') {
      const dummyToken = email.split('@')[0] + "_local_id";
      localStorage.setItem('salesbrain_token', dummyToken);
      setUser({ uid: dummyToken, email });
      router.push('/dashboard');
    } else {
      if (!auth) throw new Error('Firebase Auth is not initialized. Please check your configuration.');
      if (!password) throw new Error('Password is required in Firebase mode');
      await createUserWithEmailAndPassword(auth, email, password);
      router.push('/dashboard');
    }
  };

  const loginWithGoogle = async () => {
    if (authMode === 'local') {
      const dummyToken = "google_user_local_id";
      localStorage.setItem('salesbrain_token', dummyToken);
      setUser({ uid: dummyToken, email: 'google@salesbrain.ai' });
      router.push('/dashboard');
    } else {
      if (!auth) throw new Error('Firebase Auth is not initialized.');
      const provider = new GoogleAuthProvider();
      await signInWithPopup(auth, provider);
      router.push('/dashboard');
    }
  };

  const logout = async () => {
    if (authMode === 'local') {
      localStorage.removeItem('salesbrain_token');
      setUser(null);
      router.push('/login');
    } else {
      if (!auth) return;
      await signOut(auth);
      router.push('/login');
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, signup, loginWithGoogle, logout, authMode }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
