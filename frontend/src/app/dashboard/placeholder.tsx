/* eslint-disable @typescript-eslint/no-explicit-any */
import React from 'react';

export default function PlaceholderPage() {
  return (
    <div className="flex flex-col items-center justify-center h-[60vh] text-center space-y-4">
      <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mb-4">
        <svg className="w-8 h-8 text-slate-400" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
      </div>
      <h2 className="text-2xl font-bold text-slate-900">Module Coming Soon</h2>
      <p className="text-slate-500 max-w-md">
        This intelligence module is currently being connected to the backend ML pipeline.
      </p>
    </div>
  );
}
