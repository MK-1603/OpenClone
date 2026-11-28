import React from "react";

export const FinoraExecutiveDashboard: React.FC = () => {
  return (
    <div className="min-h-screen bg-[#0B0F19] text-[#F3F4F6] font-sans antialiased p-6">
      {/* Institutional Header */}
      <header className="flex justify-between items-center pb-6 border-b border-[#1F2937]">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded bg-[#10B981] flex items-center justify-center font-bold text-black text-sm">
            F
          </div>
          <div>
            <h1 className="text-base font-semibold tracking-tight text-[#F9FAFB]">Finora Wealth Management</h1>
            <p className="text-xs text-[#9CA3AF]">Account ID: ACC-89412-US &bull; Base Currency: USD</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-xs bg-[#1F2937] text-[#9CA3AF] px-2.5 py-1 rounded font-mono">Market Open</span>
          <button className="px-3 py-1.5 bg-[#10B981] text-black font-semibold text-xs rounded hover:bg-[#059669] transition">
            Transfer Funds
          </button>
        </div>
      </header>

      {/* High-Density Wealth Command Strip */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-4 my-6">
        <div className="bg-[#111827] border border-[#1F2937] rounded-md p-4">
          <div className="text-xs uppercase tracking-wider text-[#9CA3AF] font-medium">Total Net Worth</div>
          <div className="text-2xl font-bold font-mono tracking-tight text-[#F9FAFB] mt-1 tabular-nums">$248,390.45</div>
          <div className="text-xs font-mono text-[#10B981] mt-1.5 flex items-center">
            <span>&uarr; +$10,240.20 (+4.29%)</span>
            <span className="text-[#6B7280] ml-2">Past 30 Days</span>
          </div>
        </div>

        <div className="bg-[#111827] border border-[#1F2937] rounded-md p-4">
          <div className="text-xs uppercase tracking-wider text-[#9CA3AF] font-medium">Liquid Reserves & Runway</div>
          <div className="text-2xl font-bold font-mono tracking-tight text-[#F9FAFB] mt-1 tabular-nums">$65,990.00</div>
          <div className="text-xs font-mono text-[#9CA3AF] mt-1.5">
            <span>16.0 Months Buffer at current burn rate</span>
          </div>
        </div>

        <div className="bg-[#111827] border border-[#1F2937] rounded-md p-4">
          <div className="text-xs uppercase tracking-wider text-[#9CA3AF] font-medium">Invested Capital</div>
          <div className="text-2xl font-bold font-mono tracking-tight text-[#F9FAFB] mt-1 tabular-nums">$182,400.45</div>
          <div className="text-xs font-mono text-[#10B981] mt-1.5">
            <span>Annualized Yield: 9.42%</span>
          </div>
        </div>
      </section>

      {/* Asset Allocation & Dense Transaction Ledger */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-[#111827] border border-[#1F2937] rounded-md p-4">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-sm font-semibold text-[#F9FAFB]">Settled Ledger & Holdings</h2>
            <div className="text-xs text-[#9CA3AF] font-mono">14 Positions Active</div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-[#D1D5DB]">
              <thead className="bg-[#1F2937] text-[#9CA3AF] font-mono uppercase text-[10px]">
                <tr>
                  <th className="py-2.5 px-3">Asset Symbol</th>
                  <th className="py-2.5 px-3">Asset Class</th>
                  <th className="py-2.5 px-3 text-right">Units</th>
                  <th className="py-2.5 px-3 text-right">Market Value</th>
                  <th className="py-2.5 px-3 text-right">Unrealized P&amp;L</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1F2937] font-mono">
                <tr className="hover:bg-[#1A2234]">
                  <td className="py-3 px-3 font-semibold text-white">VTI &bull; Vanguard Total Stock</td>
                  <td className="py-3 px-3 text-[#9CA3AF]">US Equities</td>
                  <td className="py-3 px-3 text-right tabular-nums">340.00</td>
                  <td className="py-3 px-3 text-right tabular-nums font-semibold text-white">$92,480.00</td>
                  <td className="py-3 px-3 text-right tabular-nums text-[#10B981]">+$14,210.00</td>
                </tr>
                <tr className="hover:bg-[#1A2234]">
                  <td className="py-3 px-3 font-semibold text-white">VXUS &bull; Vanguard Total Intl</td>
                  <td className="py-3 px-3 text-[#9CA3AF]">Intl Equities</td>
                  <td className="py-3 px-3 text-right tabular-nums">620.00</td>
                  <td className="py-3 px-3 text-right tabular-nums font-semibold text-white">$41,540.00</td>
                  <td className="py-3 px-3 text-right tabular-nums text-[#10B981]">+$3,120.00</td>
                </tr>
                <tr className="hover:bg-[#1A2234]">
                  <td className="py-3 px-3 font-semibold text-white">BND &bull; Total Bond Market</td>
                  <td className="py-3 px-3 text-[#9CA3AF]">Fixed Income</td>
                  <td className="py-3 px-3 text-right tabular-nums">480.00</td>
                  <td className="py-3 px-3 text-right tabular-nums font-semibold text-white">$36,380.00</td>
                  <td className="py-3 px-3 text-right tabular-nums text-[#EF4444]">-$840.00</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div className="bg-[#111827] border border-[#1F2937] rounded-md p-4">
          <h2 className="text-sm font-semibold text-[#F9FAFB] mb-3">Portfolio Balance Breakdown</h2>
          <div className="space-y-3 font-mono text-xs">
            <div>
              <div className="flex justify-between text-[#9CA3AF] mb-1">
                <span>US Equities</span>
                <span className="tabular-nums">50.7%</span>
              </div>
              <div className="w-full bg-[#1F2937] h-1.5 rounded-full overflow-hidden">
                <div className="bg-[#10B981] h-1.5" style={{ width: "50.7%" }} />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-[#9CA3AF] mb-1">
                <span>Cash &amp; Equivalents</span>
                <span className="tabular-nums">26.5%</span>
              </div>
              <div className="w-full bg-[#1F2937] h-1.5 rounded-full overflow-hidden">
                <div className="bg-[#3B82F6] h-1.5" style={{ width: "26.5%" }} />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-[#9CA3AF] mb-1">
                <span>Intl Equities</span>
                <span className="tabular-nums">16.7%</span>
              </div>
              <div className="w-full bg-[#1F2937] h-1.5 rounded-full overflow-hidden">
                <div className="bg-[#8B5CF6] h-1.5" style={{ width: "16.7%" }} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
