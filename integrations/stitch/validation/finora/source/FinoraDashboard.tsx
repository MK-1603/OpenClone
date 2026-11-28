// Baseline Finora Personal Finance Dashboard
// Contains typical uninspired AI dashboard patterns:
// 1. Mindless 4-card KPI row
// 2. Generic purple gradient blob
// 3. Low-density table without tabular-nums
import React from "react";

export const FinoraDashboard: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-white p-8">
      {/* Generic Purple Gradient Blob */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-purple-600/30 rounded-full blur-3xl -z-10" />

      <header className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-indigo-500 bg-clip-text text-transparent">
            Finora Wealth
          </h1>
          <p className="text-sm text-slate-400">Personal Wealth Overview</p>
        </div>
        <button className="px-4 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 rounded-lg text-sm font-medium">
          + Add Account
        </button>
      </header>

      {/* Cliché 4-Card KPI arrangement */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="p-6 rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10">
          <p className="text-xs text-slate-400 uppercase font-medium">Net Worth</p>
          <h2 className="text-3xl font-bold mt-2">$248,390</h2>
          <span className="text-xs text-emerald-400 mt-2 block">+4.2% this month</span>
        </div>
        <div className="p-6 rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10">
          <p className="text-xs text-slate-400 uppercase font-medium">Investments</p>
          <h2 className="text-3xl font-bold mt-2">$182,400</h2>
          <span className="text-xs text-emerald-400 mt-2 block">+8.1% all-time</span>
        </div>
        <div className="p-6 rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10">
          <p className="text-xs text-slate-400 uppercase font-medium">Cash Balance</p>
          <h2 className="text-3xl font-bold mt-2">$65,990</h2>
          <span className="text-xs text-slate-400 mt-2 block">Across 3 banks</span>
        </div>
        <div className="p-6 rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10">
          <p className="text-xs text-slate-400 uppercase font-medium">Monthly Burn</p>
          <h2 className="text-3xl font-bold mt-2">$4,120</h2>
          <span className="text-xs text-rose-400 mt-2 block">-12% vs last month</span>
        </div>
      </div>

      {/* Basic table */}
      <div className="rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10 p-6">
        <h3 className="text-lg font-semibold mb-4">Recent Transactions</h3>
        <table className="w-full text-left text-sm text-slate-300">
          <thead className="text-xs text-slate-500 border-b border-white/10">
            <tr>
              <th className="pb-3">Description</th>
              <th className="pb-3">Category</th>
              <th className="pb-3">Date</th>
              <th className="pb-3 text-right">Amount</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            <tr>
              <td className="py-4">Vanguard Total Stock ETF</td>
              <td className="py-4">Investment</td>
              <td className="py-4">Nov 24, 2026</td>
              <td className="py-4 text-right text-emerald-400">+$2,500.00</td>
            </tr>
            <tr>
              <td className="py-4">Apex Cloud Hosting</td>
              <td className="py-4">Software</td>
              <td className="py-4">Nov 22, 2026</td>
              <td className="py-4 text-right text-rose-400">-$120.00</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};
