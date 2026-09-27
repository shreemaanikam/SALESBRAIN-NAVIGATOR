/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { SlidersHorizontal, Calculator, Activity, ArrowRight, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { simulate as simulateApi } from '@/services/api';

export default function WhatIfSimulatorPage() {
  const [discount, setDiscount] = useState(15);
  const [demandShock, setDemandShock] = useState(0);
  const [shippingIncrease, setShippingIncrease] = useState(0);
  const [loading, setLoading] = useState(false);
  const [apiResult, setApiResult] = useState<any>(null);

  // Baseline real dataset metrics
  const baselineSales = 12642905;
  const baselineProfit = 1469035;
  const baselineMargin = 11.62;

  const handleSimulate = async () => {
    setLoading(true);
    try {
      const res = await simulateApi({
        baseline: { category: 'All', sub_category: 'All', segment: 'All', region: 'All', market: 'All', ship_mode: 'All', sales: baselineSales, quantity: 1000, discount: 0.15, shipping_cost: 1000 },
        scenario: { discount_delta: discount - 15, quantity_change_pct: demandShock, shipping_cost_change_pct: shippingIncrease }
      });
      setApiResult(res);
    } catch {
      console.warn("API simulation failed, using fallback");
      setApiResult(null);
    } finally {
      setLoading(false);
    }
  };

  // Extremely simplified simulation calculation for demo purposes
  const simulatedSales = (apiResult as { scenario?: { sales: number, margin: number, profit: number } })?.scenario?.sales ?? (baselineSales * (1 + (demandShock / 100)) * (1 - (discount / 100)));
  const profitMarginImpact = - (discount / 2) - (shippingIncrease / 10);
  const simulatedMargin = (apiResult as { scenario?: { sales: number, margin: number, profit: number } })?.scenario?.margin ?? (baselineMargin + profitMarginImpact);
  const simulatedProfit = (apiResult as { scenario?: { sales: number, margin: number, profit: number } })?.scenario?.profit ?? (simulatedSales * (simulatedMargin / 100));

  const salesDelta = simulatedSales - baselineSales;
  const profitDelta = simulatedProfit - baselineProfit;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white flex items-center gap-3">
            <SlidersHorizontal className="w-8 h-8 text-indigo-600" />
            What-If Simulator
          </h1>
          <p className="text-slate-500 dark:text-slate-400">Test the impact of pricing and supply chain shocks.</p>
        </div>
      </div>

      <div className="bg-indigo-50 dark:bg-indigo-900/30 border border-indigo-100 dark:border-indigo-800 p-4 rounded-lg flex items-start gap-4">
        <Activity className="w-5 h-5 text-indigo-600 dark:text-indigo-400 shrink-0 mt-0.5" />
        <div>
          <h4 className="text-sm font-bold text-indigo-900 dark:text-indigo-300">Demo Simulation Mode Active</h4>
          <p className="text-sm text-indigo-700 dark:text-indigo-400">
            Currently using a rule-based simulation algorithm. This will be replaced by the ML Prediction Pipeline once the backend is integrated.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <Card className="dark:bg-slate-900 dark:border-slate-800">
            <CardHeader>
              <CardTitle className="dark:text-white">Parameters</CardTitle>
              <CardDescription className="dark:text-slate-400">Adjust the scenario constraints.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-3">
                <div className="flex justify-between">
                  <label className="text-sm font-medium text-slate-700 dark:text-slate-300">Global Discount Rate</label>
                  <span className="text-sm font-bold text-blue-600">{discount}%</span>
                </div>
                <input 
                  type="range" 
                  min="0" max="50" step="1"
                  value={discount}
                  onChange={(e) => setDiscount(Number(e.target.value))}
                  className="w-full accent-blue-600"
                />
              </div>

              <div className="space-y-3">
                <div className="flex justify-between">
                  <label className="text-sm font-medium text-slate-700 dark:text-slate-300">Demand Shock</label>
                  <span className={cn("text-sm font-bold", demandShock > 0 ? "text-green-600" : demandShock < 0 ? "text-red-600" : "text-slate-500")}>
                    {demandShock > 0 ? '+' : ''}{demandShock}%
                  </span>
                </div>
                <input 
                  type="range" 
                  min="-50" max="50" step="5"
                  value={demandShock}
                  onChange={(e) => setDemandShock(Number(e.target.value))}
                  className="w-full accent-blue-600"
                />
              </div>

              <div className="space-y-3">
                <div className="flex justify-between">
                  <label className="text-sm font-medium text-slate-700 dark:text-slate-300">Shipping Cost Increase</label>
                  <span className="text-sm font-bold text-amber-600">+{shippingIncrease}%</span>
                </div>
                <input 
                  type="range" 
                  min="0" max="100" step="5"
                  value={shippingIncrease}
                  onChange={(e) => setShippingIncrease(Number(e.target.value))}
                  className="w-full accent-blue-600"
                />
              </div>

              <div className="pt-4 mt-4 border-t border-slate-100 dark:border-slate-800 flex gap-2">
                <button 
                  onClick={() => { setDiscount(15); setDemandShock(0); setShippingIncrease(0); setApiResult(null); }}
                  className="w-1/3 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-800 rounded-md hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
                >
                  Reset
                </button>
                <button 
                  onClick={handleSimulate}
                  disabled={loading}
                  className="w-2/3 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                >
                  {loading && <Loader2 className="w-4 h-4 animate-spin" />}
                  Simulate
                </button>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="lg:col-span-2 space-y-6">
          <Card className="dark:bg-slate-900 dark:border-slate-800">
            <CardHeader className="border-b border-slate-100 dark:border-slate-800 pb-4">
              <CardTitle className="dark:text-white flex items-center gap-2">
                <Calculator className="w-5 h-5 text-blue-600" />
                Impact Analysis
              </CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <div className="grid grid-cols-1 md:grid-cols-3 divide-y md:divide-y-0 md:divide-x divide-slate-100 dark:divide-slate-800">
                
                {/* Revenue */}
                <div className="p-6">
                  <div className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-4">Projected Revenue</div>
                  <div className="text-3xl font-bold text-slate-900 dark:text-white mb-2">
                    ${(simulatedSales / 1000000).toFixed(2)}M
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <span className="text-slate-400 line-through">${(baselineSales / 1000000).toFixed(2)}M</span>
                    <ArrowRight className="w-4 h-4 text-slate-300" />
                    <span className={cn("font-bold", salesDelta >= 0 ? "text-green-600" : "text-red-600")}>
                      {salesDelta > 0 ? '+' : ''}{(salesDelta / 1000000).toFixed(2)}M
                    </span>
                  </div>
                </div>

                {/* Profit */}
                <div className="p-6">
                  <div className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-4">Projected Profit</div>
                  <div className={cn("text-3xl font-bold mb-2", simulatedProfit < 0 ? "text-red-600" : "text-slate-900 dark:text-white")}>
                    ${(simulatedProfit / 1000).toFixed(0)}k
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <span className="text-slate-400 line-through">${(baselineProfit / 1000).toFixed(0)}k</span>
                    <ArrowRight className="w-4 h-4 text-slate-300" />
                    <span className={cn("font-bold", profitDelta >= 0 ? "text-green-600" : "text-red-600")}>
                      {profitDelta > 0 ? '+' : ''}{(profitDelta / 1000).toFixed(0)}k
                    </span>
                  </div>
                </div>

                {/* Margin */}
                <div className="p-6 bg-slate-50 dark:bg-slate-800/50">
                  <div className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-4">Projected Margin</div>
                  <div className={cn("text-3xl font-bold mb-2", simulatedMargin < 0 ? "text-red-600" : "text-slate-900 dark:text-white")}>
                    {simulatedMargin.toFixed(2)}%
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <span className="text-slate-400 line-through">{baselineMargin.toFixed(2)}%</span>
                    <ArrowRight className="w-4 h-4 text-slate-300" />
                    <span className={cn("font-bold", simulatedMargin >= baselineMargin ? "text-green-600" : "text-red-600")}>
                      {simulatedMargin >= baselineMargin ? '+' : ''}{(simulatedMargin - baselineMargin).toFixed(2)}%
                    </span>
                  </div>
                </div>

              </div>
            </CardContent>
          </Card>

          <Card className="dark:bg-slate-900 dark:border-slate-800 border-l-4 border-l-amber-500">
            <CardContent className="p-6">
              <h4 className="text-lg font-bold text-slate-900 dark:text-white mb-2">Scenario Risk Evaluation</h4>
              {simulatedMargin < 5 ? (
                <p className="text-red-600 dark:text-red-400 font-medium">Critical Risk: Margin compression threatens viability. This scenario results in unsustainable profitability.</p>
              ) : simulatedMargin < baselineMargin ? (
                <p className="text-amber-600 dark:text-amber-400 font-medium">Elevated Risk: Scenario decreases margin compared to baseline. Monitor volume closely to ensure absolute profit growth.</p>
              ) : (
                <p className="text-green-600 dark:text-green-400 font-medium">Low Risk: This scenario improves margin metrics safely.</p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
