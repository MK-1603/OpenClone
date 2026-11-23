"use client";

import React, { useState } from "react";
import {
  Activity as ActivityIcon,
  CheckCircle2,
  FolderPlus,
  RefreshCw,
  Award,
  UserPlus,
  Filter,
} from "lucide-react";
import { usePulse } from "@/context/PulseContext";

export const ActivityView: React.FC = () => {
  const { activities } = usePulse();
  const [typeFilter, setTypeFilter] = useState("all");

  const filtered = activities.filter((act) => {
    if (typeFilter === "all") return true;
    if (typeFilter === "tasks") return act.type.startsWith("task_");
    if (typeFilter === "projects") return act.type === "project_created";
    if (typeFilter === "milestones") return act.type === "milestone_reached";
    return true;
  });

  const getIcon = (type: string) => {
    switch (type) {
      case "task_completed":
        return <CheckCircle2 className="w-4 h-4 text-[#10B981]" />;
      case "task_status_changed":
        return <RefreshCw className="w-4 h-4 text-[#60A5FA]" />;
      case "project_created":
        return <FolderPlus className="w-4 h-4 text-[#D6B36A]" />;
      case "milestone_reached":
        return <Award className="w-4 h-4 text-[#A855F7]" />;
      case "member_assigned":
        return <UserPlus className="w-4 h-4 text-[#F59E0B]" />;
      default:
        return <ActivityIcon className="w-4 h-4 text-[#71717A]" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header and Filter */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-xl bg-[#111111] border border-[rgba(255,255,255,0.07)]">
        <div>
          <h2 className="text-sm font-semibold text-[#F5F5F5]">Project Execution & Audit Stream</h2>
          <p className="text-[11px] text-[#71717A]">
            Chronological audit trail of all task transitions, project allocations, and milestones
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Filter className="w-3.5 h-3.5 text-[#71717A]" />
          <select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            className="px-3 py-1.5 text-xs text-[#A1A1AA] bg-[#161616] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none"
          >
            <option value="all">All Events</option>
            <option value="tasks">Task Updates</option>
            <option value="projects">Project Creation</option>
            <option value="milestones">Milestones</option>
          </select>
        </div>
      </div>

      {/* Chronological Timeline */}
      <div className="p-6 rounded-2xl bg-[#111111] border border-[rgba(255,255,255,0.08)]">
        <div className="relative pl-6 space-y-6 before:absolute before:left-2.5 before:top-3 before:bottom-3 before:w-[1px] before:bg-[rgba(255,255,255,0.08)]">
          {filtered.map((act) => (
            <div key={act.id} className="relative flex items-start gap-4 group">
              {/* Event Node Indicator */}
              <div className="absolute -left-6 mt-1 flex items-center justify-center w-5 h-5 rounded-full bg-[#161616] border border-[rgba(255,255,255,0.15)] group-hover:border-[#D6B36A] transition-colors shadow-sm">
                <div className="w-1.5 h-1.5 rounded-full bg-[#D6B36A]" />
              </div>

              {/* Event Content Card */}
              <div className="flex-1 p-4 rounded-xl bg-[#141414] hover:bg-[#171717] border border-[rgba(255,255,255,0.05)] transition-all">
                <div className="flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2">
                    <span className="p-1 rounded bg-[#202020] border border-[rgba(255,255,255,0.04)]">
                      {getIcon(act.type)}
                    </span>
                    <span className="font-semibold text-[#F5F5F5]">{act.title}</span>
                  </div>
                  <span className="text-[10px] text-[#71717A] font-mono">{act.timestamp}</span>
                </div>

                <p className="mt-1.5 text-xs text-[#A1A1AA] leading-relaxed">
                  {act.description}
                </p>

                <div className="mt-3 pt-2.5 border-t border-[rgba(255,255,255,0.04)] flex items-center justify-between text-[11px] text-[#71717A]">
                  <div className="flex items-center gap-2">
                    <img
                      src={act.actor.avatar}
                      alt={act.actor.name}
                      className="w-4 h-4 rounded-full object-cover"
                    />
                    <span>{act.actor.name}</span>
                  </div>

                  {act.projectName && (
                    <span className="text-[10px] text-[#D6B36A] bg-[#221D12] px-2 py-0.5 rounded border border-[rgba(214,179,106,0.2)]">
                      {act.projectName}
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))}

          {filtered.length === 0 && (
            <div className="text-center py-12 text-xs text-[#71717A]">
              No events found matching the selected filter.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
