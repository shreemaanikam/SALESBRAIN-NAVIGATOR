import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { ArrowRight, BarChart3, Database, Shield, Zap, Target, Cpu, Activity, CheckCircle2 } from 'lucide-react';
import { DataSphere } from '@/components/DataSphere';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 selection:bg-blue-200 dark:selection:bg-blue-900 transition-colors">
      <nav className="border-b border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 backdrop-blur-xl fixed top-0 w-full z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <BarChart3 className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-xl tracking-tight text-slate-900 dark:text-white">
              SalesBrain <span className="text-blue-600">Navigator</span>
            </span>
          </div>
          <div className="hidden md:flex items-center gap-8">
            <a href="#features" className="text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white transition-colors">Product Capabilities</a>
            <a href="#how-it-works" className="text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white transition-colors">How it Works</a>
            <a href="#security" className="text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white transition-colors">Security</a>
            <Link href="/dashboard" className="text-sm font-medium px-4 py-2 bg-slate-900 dark:bg-white text-white dark:text-slate-900 rounded-full hover:bg-slate-800 dark:hover:bg-slate-100 transition-all">
              Live Demo
            </Link>
          </div>
        </div>
      </nav>

      <main className="pt-32 pb-16">
        {/* Hero Section */}
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 text-sm font-medium mb-8 border border-blue-100 dark:border-blue-800">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
            </span>
            Enterprise Retail Intelligence v1.0
          </div>
          
          <h1 className="text-5xl md:text-7xl font-extrabold text-slate-900 dark:text-white tracking-tight mb-8 max-w-4xl mx-auto leading-tight">
            Turn retail complexity into <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">profitable decisions.</span>
          </h1>
          
          <p className="text-xl text-slate-600 dark:text-slate-400 mb-12 max-w-2xl mx-auto leading-relaxed">
            SalesBrain Navigator is an AI-powered Decision Support System that analyzes sales, profitability, risk, and opportunities across your entire global dataset.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-20">
            <Link 
              href="/dashboard"
              className="w-full sm:w-auto px-8 py-4 bg-blue-600 text-white rounded-full font-semibold text-lg hover:bg-blue-700 hover:shadow-lg hover:shadow-blue-500/30 transition-all flex items-center justify-center gap-2"
            >
              Explore Dashboard <ArrowRight className="w-5 h-5" />
            </Link>
            <Link 
              href="#contact"
              className="w-full sm:w-auto px-8 py-4 bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 rounded-full font-semibold text-lg hover:bg-slate-50 dark:hover:bg-slate-700 transition-all"
            >
              Request Demo
            </Link>
          </div>

          <div className="w-full max-w-5xl mx-auto relative rounded-2xl overflow-hidden shadow-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-2">
             {/* 3D Sphere Element */}
             <div className="absolute inset-0 z-0 opacity-50 dark:opacity-30 mix-blend-multiply dark:mix-blend-screen pointer-events-none">
               <DataSphere />
             </div>
             <Image width={800} height={600} 
              unoptimized={true}
              src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=2000" 
              alt="Dashboard Preview" 
              className="w-full h-auto rounded-xl border border-slate-100 dark:border-slate-800 relative z-10 opacity-90"
            />
          </div>
        </section>

        {/* Product Capabilities Section */}
        <section id="features" className="py-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-4">Enterprise Capabilities</h2>
            <p className="text-lg text-slate-600 dark:text-slate-400">Everything you need to run a data-driven retail operation.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white dark:bg-slate-800 p-8 rounded-2xl border border-slate-200 dark:border-slate-700 hover:shadow-xl transition-all">
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/50 rounded-xl flex items-center justify-center mb-6">
                <Target className="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3">Product Intelligence</h3>
              <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                Deep SKU-level analysis to identify loss-leaders, margin compression, and optimization opportunities.
              </p>
            </div>
            
            <div className="bg-white dark:bg-slate-800 p-8 rounded-2xl border border-slate-200 dark:border-slate-700 hover:shadow-xl transition-all">
              <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/50 rounded-xl flex items-center justify-center mb-6">
                <Cpu className="w-6 h-6 text-purple-600 dark:text-purple-400" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3">AI Decision Support</h3>
              <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                Rule-based data insights, risk flagging, and prescriptive recommendations alongside ML-powered profit prediction.
              </p>
            </div>

            <div className="bg-white dark:bg-slate-800 p-8 rounded-2xl border border-slate-200 dark:border-slate-700 hover:shadow-xl transition-all">
              <div className="w-12 h-12 bg-emerald-100 dark:bg-emerald-900/50 rounded-xl flex items-center justify-center mb-6">
                <Zap className="w-6 h-6 text-emerald-600 dark:text-emerald-400" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3">What-If Simulation</h3>
              <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                Test the impact of discount strategies and demand shocks before deploying them in the real world.
              </p>
            </div>
          </div>
        
        </section>

        {/* ── How it Works ── */}
        <section id="how-it-works" className="py-24 bg-slate-50 dark:bg-slate-800/50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-4">How SalesBrain Works</h2>
              <p className="text-xl text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">From raw data to actionable insights in three simple steps.</p>
            </div>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="bg-white dark:bg-slate-900 p-8 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-800">
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400 rounded-full flex items-center justify-center font-bold text-xl mb-6">1</div>
                <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3">Connect Data</h3>
                <p className="text-slate-600 dark:text-slate-400">Upload your CSV dataset. SalesBrain securely processes it locally without sending it to external APIs.</p>
              </div>
              <div className="bg-white dark:bg-slate-900 p-8 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-800">
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400 rounded-full flex items-center justify-center font-bold text-xl mb-6">2</div>
                <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3">Auto-Generate KPIs</h3>
                <p className="text-slate-600 dark:text-slate-400">Our engine instantly creates a dynamic dashboard with your revenue, margins, and regional performance trends.</p>
              </div>
              <div className="bg-white dark:bg-slate-900 p-8 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-800">
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400 rounded-full flex items-center justify-center font-bold text-xl mb-6">3</div>
                <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3">Generate Data Insights & Profit Predictions</h3>
                <p className="text-slate-600 dark:text-slate-400">Leverage our Ridge regression models to predict profitability and uncover hidden growth opportunities.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Security Section */}

        <section id="security" className="py-24 bg-slate-900 text-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex flex-col md:flex-row items-center gap-12">
              <div className="flex-1">
                <div className="w-16 h-16 bg-blue-600/20 rounded-2xl flex items-center justify-center mb-6 border border-blue-500/30">
                  <Shield className="w-8 h-8 text-blue-400" />
                </div>
                <h2 className="text-3xl font-bold mb-6">Enterprise-Grade Security & Data Handling</h2>
                <p className="text-slate-400 text-lg mb-8 leading-relaxed">
                  SalesBrain Navigator processes uploaded datasets through its authenticated backend analytics pipeline and stores workspace data in configured persistent storage. Authenticated access and per-user workspace isolation protect workspace operations.
                </p>
                <ul className="space-y-4">
                  <li className="flex items-center gap-3 text-slate-300">
                    <Database className="w-5 h-5 text-blue-400" /> Secure Data Pipeline Integration
                  </li>
                  <li className="flex items-center gap-3 text-slate-300">
                    <Shield className="w-5 h-5 text-blue-400" /> Authenticated Access & Tenant Isolation
                  </li>
                </ul>
              </div>
              <div className="flex-1 w-full bg-slate-800 rounded-2xl p-8 border border-slate-700">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="bg-slate-700/50 p-4 rounded-lg border border-slate-600">
                    <h4 className="text-white font-semibold flex items-center gap-2 mb-2"><Database className="w-4 h-4 text-blue-400"/> Data Handling</h4>
                    <p className="text-slate-300 text-sm">Data is processed locally within your environment. No sensitive business metrics are transmitted to external third-party servers.</p>
                  </div>
                  <div className="bg-slate-700/50 p-4 rounded-lg border border-slate-600">
                    <h4 className="text-white font-semibold flex items-center gap-2 mb-2"><Shield className="w-4 h-4 text-blue-400"/> Privacy</h4>
                    <p className="text-slate-300 text-sm">Customer information is handled according to internal data policies. Personal identifiable information is aggregated prior to modeling.</p>
                  </div>
                  <div className="bg-slate-700/50 p-4 rounded-lg border border-slate-600">
                    <h4 className="text-white font-semibold flex items-center gap-2 mb-2"><Activity className="w-4 h-4 text-blue-400"/> Security Configuration</h4>
                    <p className="text-slate-300 text-sm">Deployment settings follow standard secure-by-default configurations for the local analytic pipeline.</p>
                  </div>
                  <div className="bg-slate-700/50 p-4 rounded-lg border border-slate-600">
                    <h4 className="text-white font-semibold flex items-center gap-2 mb-2"><CheckCircle2 className="w-4 h-4 text-blue-400"/> Access Management</h4>
                    <p className="text-slate-300 text-sm">Built to integrate with your existing corporate authentication and authorization protocols.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        
        </section>

        

        {/* ── Request Demo / Contact ── */}
        <section id="contact" className="py-24 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-6">Ready to transform your retail data?</h2>
          <p className="text-xl text-slate-600 dark:text-slate-400 mb-8">Deploy SalesBrain Navigator in your private environment and unlock the power of your data.</p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link href="/dashboard" className="px-8 py-4 bg-blue-600 text-white rounded-full font-semibold text-lg hover:bg-blue-700 transition-colors">
              Try it now
            </Link>
            <a href="mailto:demo@salesbrain.ai" className="px-8 py-4 bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white rounded-full font-semibold text-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors border border-slate-200 dark:border-slate-700">
              Contact Sales
            </a>
          </div>
        </section>
      </main>



      <footer className="bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 py-12 text-center">
        <p className="text-slate-500 dark:text-slate-400">© 2026 SalesBrain Navigator. Internal Corporate Tool.</p>
      </footer>
    </div>
  );
}
