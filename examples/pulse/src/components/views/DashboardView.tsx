"use client";

import React from "react";
import {
  TrendingUp,
  FolderKanban,
  CheckCircle2,
  Clock,
  AlertCircle,
  ArrowUpRight,
  Shield,
  Calendar,
  Sparkles,
} from "lucide-react";
import { usePulse } from "@/context/PulseContext";

export const DashboardView: React.FC<{ onNavigate: (tab: any) => void }> = ({ onNavigate }) => {
  const { projects, tasks, activities } = usePulse();

  const totalProjects = projects.length;
  const activeProjects = projects.filter((p) => p.status === "in_progress").length;
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter((t) => t.status === "completed").length;
  const completionRate = totalTasks ? Math.round((completedTasks / totalTasks) * 100) : 0;
  const urgentTasks = tasks.filter((t) => t.priority === "urgent" && t.status !== "completed");

  const weeklyData = [
    { day: "Mon", hours: 38, tasks: 6 },
    { day: "Tue", hours: 44, tasks: 9 },
    { day: "Wed", hours: 52, tasks: 12 },
    { day: "Thu", hours: 48, tasks: 8 },
    { day: "Fri", hours: 56, tasks: 14 },
    { day: "Sat", hours: 22, tasks: 4 },
    { day: "Sun", hours: 16, tasks: 3 },
  ];

  const maxHours = Math.max(...weeklyData.map((d) => d.hours));

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="relative overflow-hidden p-6 rounded-2xl bg-gradient-to-r from-[#141414] via-[#111111] to-[#0D0D0D] border border-[rgba(255,255,255,0.08)] shadow-xl">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <span className="px-2 py-0.5 text-[10px] font-semibold text-[#D6B36A] bg-[#252014] border border-[rgba(214,179,106,0.3)] rounded-full uppercase tracking-wider">
                Live Command Console
              </span>
              <span className="text-xs text-[#71717A]">Monday, November 23, 2026</span>
            </div>
            <h1 className="text-xl md:text-2xl font-bold text-[#F5F5F5] tracking-tight">
              Welcome back, Elena
            </h1>
            <p className="text-xs text-[#A1A1AA] mt-1 max-w-xl">
              "Everything in Motion. One Clear Direction." You have {urgentTasks.length} urgent tasks requiring architectural review today.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => onNavigate("tasks")}
              className="flex items-center gap-2 px-3.5 py-2 text-xs font-semibold text-[#0E0E0E] bg-[#D6B36A] hover:bg-[#E0C58A] rounded-lg shadow-sm transition-all"
            >
              <span>View Sprint Board</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => onNavigate("projects")}
              className="px-3.5 py-2 text-xs font-medium text-[#F5F5F5] bg-[#1C1C1E] hover:bg-[#252528] border border-[rgba(255,255,255,0.08)] rounded-lg transition-colors"
            >
              Portfolio Review
            </button>
          </div>
        </div>
      </div>

      {/* KPI Overview Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-[#111111] border border-[rgba(255,255,255,0.07)]">
          <div className="flex items-center justify-between text-[#71717A] text-xs">
            <span>Active Projects</span>
            <FolderKanban className="w-4 h-4 text-[#D6B36A]" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-[#F5F5F5]">{activeProjects}</span>
            <span className="text-[11px] text-[#A1A1AA]">of {totalProjects} total</span>
          </div>
          <div className="mt-2 w-full bg-[#1F1F1F] rounded-full h-1.5 overflow-hidden">
            <div
              className="bg-[#D6B36A] h-full rounded-full transition-all duration-500"
              style={{ width: `${(activeProjects / totalProjects) * 100}%` }}
            />
          </div>
        </div>

        <div className="p-4 rounded-xl bg-[#111111] border border-[rgba(255,255,255,0.07)]">
          <div className="flex items-center justify-between text-[#71717A] text-xs">
            <span>Task Completion</span>
            <CheckCircle2 className="w-4 h-4 text-[#10B981]" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-[#F5F5F5]">{completionRate}%</span>
            <span className="text-[11px] text-[#10B981]">+8% vs last week</span>
          </div>
          <div className="mt-2 w-full bg-[#1F1F1F] rounded-full h-1.5 overflow-hidden">
            <div
              className="bg-[#10B981] h-full rounded-full transition-all duration-500"
              style={{ width: `${completionRate}%` }}
            />
          </div>
        </div>

        <div className="p-4 rounded-xl bg-[#111111] border border-[rgba(255,255,255,0.07)]">
          <div className="flex items-center justify-between text-[#71717A] text-xs">
            <span>Pending Deliverables</span>
            <Clock className="w-4 h-4 text-[#F59E0B]" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-[#F5F5F5]">{totalTasks - completedTasks}</span>
            <span className="text-[11px] text-[#F59E0B]">{urgentTasks.length} urgent</span>
          </div>
          <div className="mt-2 w-full bg-[#1F1F1F] rounded-full h-1.5 overflow-hidden">
            <div
              className="bg-[#F59E0B] h-full rounded-full transition-all duration-500"
              style={{ width: `${((totalTasks - completedTasks) / totalTasks) * 100}%` }}
            />
          </div>
        </div>

        <div className="p-4 rounded-xl bg-[#111111] border border-[rgba(255,255,255,0.07)]">
          <div className="flex items-center justify-between text-[#71717A] text-xs">
            <span>Engineering Velocity</span>
            <TrendingUp className="w-4 h-4 text-[#60A5FA]" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-[#F5F5F5]">276 hrs</span>
            <span className="text-[11px] text-[#60A5FA]">logged this week</span>
          </div>
          <div className="mt-2 w-full bg-[#1F1F1F] rounded-full h-1.5 overflow-hidden">
            <div className="bg-[#60A5FA] h-full rounded-full" style={{ width: "88%" }} />
          </div>
        </div>
      </div>

      {/* Main Grid: Weekly Chart & Active Projects */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Weekly Productivity SVG Chart */}
        <div className="lg:col-span-2 p-5 rounded-2xl bg-[#111111] border border-[rgba(255,255,255,0.08)] flex flex-col justify-between">
          <div className="flex items-center justify-between pb-3 border-b border-[rgba(255,255,255,0.05)]">
            <div>
              <h3 className="text-sm font-semibold text-[#F5F5F5]">Weekly Productivity & Engineering Output</h3>
              <p className="text-[11px] text-[#71717A]">Hours committed across 6 active repositories</p>
            </div>
            <div className="flex items-center gap-2 text-xs">
              <span className="flex items-center gap-1.5 text-[11px] text-[#A1A1AA]">
                <span className="w-2.5 h-2.5 rounded-sm bg-[#D6B36A]" /> Committed Hours
              </span>
            </div>
          </div>

          {/* SVG Bar Chart */}
          <div className="pt-6 pb-2">
            <div className="flex items-end justify-between gap-3 h-48 px-2">
              {weeklyData.map((d) => {
                const heightPercent = Math.round((d.hours / maxHours) * 100);
                return (
                  <div key={d.day} className="flex-1 flex flex-col items-center gap-2 group">
                    <span className="text-[10px] text-[#71717A] opacity-0 group-hover:opacity-100 transition-opacity">
                      {d.hours}h
                    </span>
                    <div className="w-full bg-[#1A1A1A] rounded-t-md h-36 flex items-end overflow-hidden p-1">
                      <div
                        className="w-full bg-gradient-to-t from-[#B08D45] to-[#D6B36A] group-hover:to-[#EBD8AC] rounded-sm transition-all duration-300"
                        style={{ height: `${heightPercent}%` }}
                      />
                    </div>
                    <span className="text-xs text-[#A1A1AA] font-medium">{d.day}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Project Health Radar */}
        <div className="p-5 rounded-2xl bg-[#111111] border border-[rgba(255,255,255,0.08)] flex flex-col">
          <div className="flex items-center justify-between pb-3 border-b border-[rgba(255,255,255,0.05)]">
            <h3 className="text-sm font-semibold text-[#F5F5F5]">Project Health Status</h3>
            <span className="text-[10px] text-[#D6B36A] font-medium">Real-time</span>
          </div>

          <div className="mt-4 space-y-3 flex-1 overflow-y-auto">
            {projects.slice(0, 4).map((p) => (
              <div
                key={p.id}
                className="p-3 rounded-xl bg-[#161616] border border-[rgba(255,255,255,0.05)] hover:border-[rgba(214,179,106,0.3)] transition-all cursor-pointer"
                onClick={() => onNavigate("projects")}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-[#F5F5F5] truncate max-w-[170px]">
                    {p.name}
                  </span>
                  <span
                    className={`px-1.5 py-0.5 text-[9px] font-semibold rounded-full uppercase ${
                      p.health === "healthy"
                        ? "bg-[#064E3B] text-[#34D399]"
                        : "bg-[#78350F] text-[#FBBF24]"
                    }`}
                  >
                    {p.health}
                  </span>
                </div>
                <div className="mt-2 flex items-center justify-between text-[11px] text-[#71717A]">
                  <span>{p.category}</span>
                  <span className="text-[#A1A1AA] font-mono">{p.progress}%</span>
                </div>
                <div className="mt-1.5 w-full bg-[#202020] rounded-full h-1">
                  <div
                    className="bg-[#D6B36A] h-full rounded-full"
                    style={{ width: `${p.progress}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Two Column Section: Priority Tasks & Live Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Priority Deliverables */}
        <div className="p-5 rounded-2xl bg-[#111111] border border-[rgba(255,255,255,0.08)]">
          <div className="flex items-center justify-between pb-3 border-b border-[rgba(255,255,255,0.05)]">
            <h3 className="text-sm font-semibold text-[#F5F5F5]">Urgent & Priority Tasks</h3>
            <button
              onClick={() => onNavigate("tasks")}
              className="text-xs text-[#D6B36A] hover:underline"
            >
              View all tasks
            </button>
          </div>

          <div className="mt-3 space-y-2.5">
            {tasks
              .filter((t) => t.status !== "completed")
              .slice(0, 4)
              .map((task) => (
                <div
                  key={task.id}
                  className="flex items-center justify-between p-3 rounded-xl bg-[#161616] hover:bg-[#1A1A1A] border border-[rgba(255,255,255,0.04)] transition-all"
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <span
                      className={`w-2 h-2 rounded-full shrink-0 ${
                        task.priority === "urgent"
                          ? "bg-[#EF4444]"
                          : task.priority === "high"
                          ? "bg-[#F59E0B]"
                          : "bg-[#3B82F6]"
                      }`}
                    />
                    <div className="min-w-0">
                      <div className="text-xs font-medium text-[#F5F5F5] truncate">
                        {task.title}
                      </div>
                      <div className="text-[10px] text-[#71717A] truncate">
                        {task.projectName} · Due {task.dueDate}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <span className="text-[10px] px-2 py-0.5 rounded bg-[#202020] text-[#A1A1AA] border border-[rgba(255,255,255,0.05)]">
                      {task.status.replace("_", " ")}
                    </span>
                    <img
                      src={task.assignee.avatar}
                      alt={task.assignee.name}
                      className="w-5 h-5 rounded-full object-cover border border-[#27272A]"
                      title={task.assignee.name}
                    />
                  </div>
                </div>
              ))}
          </div>
        </div>

        {/* Live Activity Feed */}
        <div className="p-5 rounded-2xl bg-[#111111] border border-[rgba(255,255,255,0.08)]">
          <div className="flex items-center justify-between pb-3 border-b border-[rgba(255,255,255,0.05)]">
            <h3 className="text-sm font-semibold text-[#F5F5F5]">Recent Execution Activity</h3>
            <button
              onClick={() => onNavigate("activity")}
              className="text-xs text-[#D6B36A] hover:underline"
            >
              Full timeline
            </button>
          </div>

          <div className="mt-3 space-y-3">
            {activities.slice(0, 4).map((act) => (
              <div key={act.id} className="flex items-start gap-3 text-xs">
                <img
                  src={act.actor.avatar}
                  alt={act.actor.name}
                  className="w-6 h-6 rounded-full object-cover mt-0.5 border border-[rgba(255,255,255,0.1)] shrink-0"
                />
                <div className="min-w-0 flex-1">
                  <div className="text-[#F5F5F5] font-medium leading-tight">
                    <span className="text-[#D6B36A]">{act.actor.name}</span> {act.title}
                  </div>
                  <div className="text-[10px] text-[#71717A] mt-0.5 line-clamp-1">
                    {act.description}
                  </div>
                </div>
                <span className="text-[10px] text-[#52525B] shrink-0">{act.timestamp}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
