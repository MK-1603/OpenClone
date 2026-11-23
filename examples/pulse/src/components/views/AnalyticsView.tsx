"use client";

import React, { useState } from "react";
import {
  BarChart3,
  TrendingUp,
  PieChart as PieIcon,
  CheckCircle2,
  AlertTriangle,
  Clock,
  ArrowUpRight,
  ShieldAlert,
} from "lucide-react";
import { usePulse } from "@/context/PulseContext";

export const AnalyticsView: React.FC = () => {
  const { projects, tasks, team } = usePulse();
  const [timeRange, setTimeRange] = useState("Last 30 Days");

  const totalTasks = tasks.length;
  const completedTasks = tasks.filter((t) => t.status === "completed").length;
  const completionRate = totalTasks ? Math.round((completedTasks / totalTasks) * 100) : 0;
  const healthyProjects = projects.filter((p) => p.health === "healthy").length;

  // Sprint Velocity Data (Last 6 Sprints)
  const velocityData = [
    { sprint: "Sprint 42", planned: 40, completed: 38 },
    { sprint: "Sprint 43", planned: 45, completed: 44 },
    { sprint: "Sprint 44", planned: 48, completed: 42 },
    { sprint: "Sprint 45", planned: 50, completed: 52 },
    { sprint: "Sprint 46", planned: 55, completed: 53 },
    { sprint: "Sprint 47", planned: 60, completed: 58 },
  ];

  // Work distribution by department
  const departmentWorkload = [
    { name: "Engineering", percentage: 42, color: "#D6B36A" },
    { name: "Product & Architecture", percentage: 24, color: "#60A5FA" },
    { name: "UX / UI Design", percentage: 18, color: "#A855F7" },
    { name: "DevOps & Security", percentage: 16, color: "#10B981" },
  ];

  const maxSprint = Math.max(...velocityData.map((v) => Math.max(v.planned, v.completed)));

  return (
    <div className="space-y-6">
      {/* Analytics Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-xl bg-[#111111] border border-[rgba(255,255,255,0.07)]">
        <div>
          <h2 className="text-sm font-semibold text-[#F5F5F5]">Executive Performance Metrics</h2>
          <p className="text-[11px] text-[#71717A]">
            Engineering throughput, sprint velocity, and resource distribution
          </p>
        </div>

        <select
          value={timeRange}
          onChange={(e) => setTimeRange(e.target.value)}
          className="px-3 py-1.5 text-xs text-[#A1A1AA] bg-[#161616] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none"
        >
          <option>Last 7 Days</option>
          <option>Last 30 Days</option>
          <option>Last Quarter (Q4)</option>
          <option>Year to Date</option>
        </select>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-[#111111] border border-[rgba(255,255,255,0.07)]">
          <div className="text-[11px] text-[#71717A] flex items-center justify-between">
            <span>Overall Completion</span>
            <CheckCircle2 className="w-4 h-4 text-[#10B981]" />
          </div>
          <div className="mt-2 text-2xl font-bold text-[#F5F5F5]">{completionRate}%</div>
          <div className="mt-1 text-[10px] text-[#10B981]">+4.2% acceleration</div>
        </div>

        <div className="p-4 rounded-xl bg-[#111111] border border-[rgba(255,255,255,0.07)]">
          <div className="text-[11px] text-[#71717A] flex items-center justify-between">
            <span>Portfolio Health</span>
            <ShieldAlert className="w-4 h-4 text-[#D6B36A]" />
          </div>
          <div className="mt-2 text-2xl font-bold text-[#F5F5F5]">
            {healthyProjects}/{projects.length}
          </div>
          <div className="mt-1 text-[10px] text-[#A1A1AA]">Projects in green status</div>
        </div>

        <div className="p-4 rounded-xl bg-[#111111] border border-[rgba(255,255,255,0.07)]">
          <div className="text-[11px] text-[#71717A] flex items-center justify-between">
            <span>Sprint Burndown Rate</span>
            <TrendingUp className="w-4 h-4 text-[#60A5FA]" />
          </div>
          <div className="mt-2 text-2xl font-bold text-[#F5F5F5]">96.6%</div>
          <div className="mt-1 text-[10px] text-[#60A5FA]">Target reliability index</div>
        </div>

        <div className="p-4 rounded-xl bg-[#111111] border border-[rgba(255,255,255,0.07)]">
          <div className="text-[11px] text-[#71717A] flex items-center justify-between">
            <span>Avg Cycle Time</span>
            <Clock className="w-4 h-4 text-[#A855F7]" />
          </div>
          <div className="mt-2 text-2xl font-bold text-[#F5F5F5]">2.4 days</div>
          <div className="mt-1 text-[10px] text-[#A855F7]">-0.6d improvement</div>
        </div>
      </div>

      {/* Main Charts: Velocity Trend and Resource Allocation */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Sprint Velocity Comparison */}
        <div className="lg:col-span-2 p-5 rounded-2xl bg-[#111111] border border-[rgba(255,255,255,0.08)]">
          <div className="flex items-center justify-between pb-3 border-b border-[rgba(255,255,255,0.05)]">
            <div>
              <h3 className="text-sm font-semibold text-[#F5F5F5]">Sprint Velocity: Planned vs Delivered</h3>
              <p className="text-[11px] text-[#71717A]">Story points delivered over the past 6 engineering sprints</p>
            </div>
            <div className="flex items-center gap-4 text-[11px]">
              <span className="flex items-center gap-1.5 text-[#71717A]">
                <span className="w-2.5 h-2.5 rounded-sm bg-[#27272A]" /> Planned
              </span>
              <span className="flex items-center gap-1.5 text-[#D6B36A]">
                <span className="w-2.5 h-2.5 rounded-sm bg-[#D6B36A]" /> Delivered
              </span>
            </div>
          </div>

          <div className="pt-8 pb-3">
            <div className="flex items-end justify-between gap-4 h-52 px-3">
              {velocityData.map((v) => {
                const planHeight = Math.round((v.planned / maxSprint) * 100);
                const doneHeight = Math.round((v.completed / maxSprint) * 100);
                return (
                  <div key={v.sprint} className="flex-1 flex flex-col items-center gap-2 group">
                    <span className="text-[10px] text-[#71717A] opacity-0 group-hover:opacity-100 transition-opacity">
                      {v.completed} pts
                    </span>
                    <div className="w-full flex items-end justify-center gap-1.5 h-40">
                      {/* Planned Bar */}
                      <div
                        className="w-3.5 bg-[#27272A] rounded-t-sm transition-all"
                        style={{ height: `${planHeight}%` }}
                        title={`Planned: ${v.planned}`}
                      />
                      {/* Completed Bar */}
                      <div
                        className="w-3.5 bg-gradient-to-t from-[#B08D45] to-[#D6B36A] rounded-t-sm transition-all"
                        style={{ height: `${doneHeight}%` }}
                        title={`Delivered: ${v.completed}`}
                      />
                    </div>
                    <span className="text-[10px] text-[#A1A1AA] font-mono">{v.sprint.replace("Sprint ", "S")}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Workload Distribution */}
        <div className="p-5 rounded-2xl bg-[#111111] border border-[rgba(255,255,255,0.08)] flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-[rgba(255,255,255,0.05)]">
              <h3 className="text-sm font-semibold text-[#F5F5F5]">Work Distribution</h3>
              <PieIcon className="w-4 h-4 text-[#71717A]" />
            </div>

            <div className="mt-5 space-y-4">
              {departmentWorkload.map((dept) => (
                <div key={dept.name} className="space-y-1.5">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-[#A1A1AA]">{dept.name}</span>
                    <span className="font-mono text-[#F5F5F5] font-semibold">
                      {dept.percentage}%
                    </span>
                  </div>
                  <div className="w-full bg-[#1F1F1F] rounded-full h-1.5 overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-500"
                      style={{
                        width: `${dept.percentage}%`,
                        backgroundColor: dept.color,
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="p-3.5 mt-6 rounded-xl bg-[#161616] border border-[rgba(255,255,255,0.04)] text-xs text-[#71717A]">
            <span className="text-[#D6B36A] font-semibold">Capacity Note:</span> Engineering allocation is currently at optimal 82% utilization with zero critical bottlenecks.
          </div>
        </div>
      </div>
    </div>
  );
};
