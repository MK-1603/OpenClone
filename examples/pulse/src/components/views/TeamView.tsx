"use client";

import React, { useState } from "react";
import { Users, Mail, CheckCircle2, Clock, Search, ShieldCheck } from "lucide-react";
import { usePulse } from "@/context/PulseContext";

export const TeamView: React.FC = () => {
  const { team } = usePulse();
  const [search, setSearch] = useState("");
  const [departmentFilter, setDepartmentFilter] = useState("all");

  const departments = Array.from(new Set(team.map((m) => m.department)));

  const filteredTeam = team.filter((m) => {
    const matchesSearch =
      m.name.toLowerCase().includes(search.toLowerCase()) ||
      m.role.toLowerCase().includes(search.toLowerCase()) ||
      m.email.toLowerCase().includes(search.toLowerCase());
    const matchesDept = departmentFilter === "all" || m.department === departmentFilter;
    return matchesSearch && matchesDept;
  });

  return (
    <div className="space-y-6">
      {/* Controls Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-xl bg-[#111111] border border-[rgba(255,255,255,0.07)]">
        <div className="flex items-center gap-3 flex-1 max-w-md">
          <div className="relative w-full">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#71717A]" />
            <input
              type="text"
              placeholder="Search team members by name or role..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 text-xs text-[#F5F5F5] bg-[#161616] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none focus:border-[rgba(214,179,106,0.5)] placeholder-[#52525B]"
            />
          </div>

          <select
            value={departmentFilter}
            onChange={(e) => setDepartmentFilter(e.target.value)}
            className="px-3 py-1.5 text-xs text-[#A1A1AA] bg-[#161616] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none"
          >
            <option value="all">All Departments</option>
            {departments.map((d) => (
              <option key={d} value={d}>
                {d}
              </option>
            ))}
          </select>
        </div>

        <div className="text-xs text-[#71717A]">
          Showing <span className="text-[#F5F5F5] font-semibold">{filteredTeam.length}</span> active team members
        </div>
      </div>

      {/* Team Roster Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {filteredTeam.map((member) => (
          <div
            key={member.id}
            className="p-5 rounded-2xl bg-[#111111] hover:bg-[#141414] border border-[rgba(255,255,255,0.07)] hover:border-[rgba(214,179,106,0.3)] transition-all flex flex-col justify-between shadow-sm group"
          >
            <div>
              {/* Member Card Header */}
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="relative">
                    <img
                      src={member.avatar}
                      alt={member.name}
                      className="w-11 h-11 rounded-full object-cover border border-[rgba(255,255,255,0.15)] group-hover:border-[rgba(214,179,106,0.5)] transition-colors"
                    />
                    <span
                      className={`absolute bottom-0 right-0 w-3 h-3 rounded-full border-2 border-[#111111] ${
                        member.status === "active"
                          ? "bg-[#10B981]"
                          : member.status === "in_meeting"
                          ? "bg-[#F59E0B]"
                          : "bg-[#71717A]"
                      }`}
                      title={`Status: ${member.status.replace("_", " ")}`}
                    />
                  </div>

                  <div>
                    <h3 className="text-xs font-semibold text-[#F5F5F5] group-hover:text-[#D6B36A] transition-colors">
                      {member.name}
                    </h3>
                    <p className="text-[11px] text-[#A1A1AA] line-clamp-1">{member.role}</p>
                    <span className="text-[10px] text-[#71717A]">{member.department}</span>
                  </div>
                </div>

                <a
                  href={`mailto:${member.email}`}
                  className="p-1.5 rounded-lg text-[#71717A] hover:text-[#D6B36A] hover:bg-[#1C1C1E] transition-colors"
                  title={member.email}
                >
                  <Mail className="w-3.5 h-3.5" />
                </a>
              </div>

              {/* Task Counts */}
              <div className="mt-4 grid grid-cols-2 gap-2 text-center">
                <div className="p-2 rounded-xl bg-[#161616] border border-[rgba(255,255,255,0.04)]">
                  <span className="text-sm font-semibold text-[#F5F5F5]">{member.activeTasks}</span>
                  <span className="block text-[9px] text-[#71717A] uppercase tracking-wider">Active</span>
                </div>
                <div className="p-2 rounded-xl bg-[#161616] border border-[rgba(255,255,255,0.04)]">
                  <span className="text-sm font-semibold text-[#10B981]">{member.completedTasks}</span>
                  <span className="block text-[9px] text-[#71717A] uppercase tracking-wider">Shipped</span>
                </div>
              </div>
            </div>

            {/* Workload Indicator */}
            <div className="mt-4 pt-3 border-t border-[rgba(255,255,255,0.05)]">
              <div className="flex items-center justify-between text-[11px] mb-1.5">
                <span className="text-[#71717A]">Workload Utilization</span>
                <span
                  className={`font-mono font-medium ${
                    member.workloadPercent >= 85
                      ? "text-[#F59E0B]"
                      : "text-[#D6B36A]"
                  }`}
                >
                  {member.workloadPercent}%
                </span>
              </div>
              <div className="w-full bg-[#1F1F1F] rounded-full h-1.5 overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-300"
                  style={{
                    width: `${member.workloadPercent}%`,
                    backgroundColor: member.workloadPercent >= 85 ? "#F59E0B" : "#D6B36A",
                  }}
                />
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
