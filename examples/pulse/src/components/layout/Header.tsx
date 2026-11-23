"use client";

import React, { useState } from "react";
import { Search, Plus, Bell, ChevronRight, Check } from "lucide-react";
import { usePulse } from "@/context/PulseContext";

interface HeaderProps {
  currentTab: string;
  onOpenQuickCreate: () => void;
}

export const Header: React.FC<HeaderProps> = ({ currentTab, onOpenQuickCreate }) => {
  const { searchQuery, setSearchQuery, activities, team } = usePulse();
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [profileMenuOpen, setProfileMenuOpen] = useState(false);

  const currentUser = team[0]; // Elena Rostova

  const tabLabels: Record<string, string> = {
    dashboard: "Dashboard Overview",
    projects: "Project Portfolio",
    tasks: "Task Management Board",
    calendar: "Schedule & Deadlines",
    analytics: "Engineering Velocity & Analytics",
    team: "Team Roster & Workload",
    activity: "Audit Activity Log",
    settings: "Workspace Settings",
  };

  return (
    <header className="flex items-center justify-between h-16 px-6 bg-[#0E0E0E] border-b border-[rgba(255,255,255,0.08)] select-none z-20">
      {/* Breadcrumb Navigation */}
      <div className="flex items-center gap-2 text-xs">
        <span className="text-[#71717A] hover:text-[#A1A1AA] cursor-pointer">PULSE</span>
        <ChevronRight className="w-3.5 h-3.5 text-[#52525B]" />
        <span className="font-semibold text-[#F5F5F5] tracking-wide">
          {tabLabels[currentTab] || "Overview"}
        </span>
      </div>

      {/* Global Actions */}
      <div className="flex items-center gap-3">
        {/* Search Bar */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#71717A]" />
          <input
            type="text"
            placeholder="Search projects, tasks, team... (Ctrl+K)"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-64 md:w-80 pl-9 pr-3 py-1.5 text-xs text-[#F5F5F5] bg-[#141414] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none focus:border-[rgba(214,179,106,0.4)] placeholder-[#52525B] transition-all"
          />
        </div>

        {/* Quick Create Action */}
        <button
          onClick={onOpenQuickCreate}
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-[#0E0E0E] bg-[#D6B36A] hover:bg-[#E0C58A] rounded-lg shadow-sm transition-all"
        >
          <Plus className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">New Item</span>
        </button>

        {/* Notifications Button */}
        <div className="relative">
          <button
            onClick={() => setNotificationsOpen(!notificationsOpen)}
            className="relative p-2 rounded-lg text-[#A1A1AA] hover:text-[#F5F5F5] hover:bg-[#181818] border border-transparent hover:border-[rgba(255,255,255,0.06)] transition-colors"
            title="Notifications"
          >
            <Bell className="w-4 h-4" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-[#D6B36A]" />
          </button>

          {/* Notifications Flyout */}
          {notificationsOpen && (
            <div className="absolute right-0 top-12 w-80 bg-[#161616] border border-[rgba(255,255,255,0.12)] rounded-xl shadow-2xl p-3 z-50 animate-in fade-in zoom-in-95 duration-150">
              <div className="flex items-center justify-between pb-2 mb-2 border-b border-[rgba(255,255,255,0.08)]">
                <span className="text-xs font-semibold text-[#F5F5F5]">Activity Alerts</span>
                <span className="text-[10px] text-[#D6B36A] font-medium cursor-pointer hover:underline">
                  Mark all read
                </span>
              </div>
              <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
                {activities.slice(0, 4).map((act) => (
                  <div
                    key={act.id}
                    className="p-2 rounded-lg bg-[#1B1B1B] hover:bg-[#222222] border border-[rgba(255,255,255,0.04)] transition-colors text-xs"
                  >
                    <div className="font-medium text-[#F5F5F5] truncate">{act.title}</div>
                    <div className="text-[10px] text-[#A1A1AA] line-clamp-1 mt-0.5">
                      {act.description}
                    </div>
                    <div className="text-[9px] text-[#71717A] mt-1">{act.timestamp}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* User Profile */}
        <div className="relative">
          <button
            onClick={() => setProfileMenuOpen(!profileMenuOpen)}
            className="flex items-center gap-2 p-1 pl-2 rounded-lg bg-[#141414] hover:bg-[#1A1A1A] border border-[rgba(255,255,255,0.06)] transition-all"
          >
            <span className="hidden md:inline text-xs font-medium text-[#F5F5F5]">
              {currentUser.name}
            </span>
            <img
              src={currentUser.avatar}
              alt={currentUser.name}
              className="w-6 h-6 rounded-full object-cover border border-[rgba(214,179,106,0.4)]"
            />
          </button>

          {profileMenuOpen && (
            <div className="absolute right-0 top-12 w-56 bg-[#161616] border border-[rgba(255,255,255,0.12)] rounded-xl shadow-2xl p-2 z-50">
              <div className="px-3 py-2 border-b border-[rgba(255,255,255,0.06)]">
                <div className="text-xs font-semibold text-[#F5F5F5]">{currentUser.name}</div>
                <div className="text-[10px] text-[#71717A]">{currentUser.email}</div>
              </div>
              <div className="py-1">
                <div className="px-3 py-1.5 text-xs text-[#A1A1AA] hover:bg-[#202020] rounded-md cursor-pointer">
                  Account Settings
                </div>
                <div className="px-3 py-1.5 text-xs text-[#A1A1AA] hover:bg-[#202020] rounded-md cursor-pointer">
                  Team Members
                </div>
                <div className="px-3 py-1.5 text-xs text-[#A1A1AA] hover:bg-[#202020] rounded-md cursor-pointer">
                  Governance Audit Key
                </div>
              </div>
              <div className="pt-1 mt-1 border-t border-[rgba(255,255,255,0.06)]">
                <div className="px-3 py-1.5 text-xs text-[#EF4444] hover:bg-[#281515] rounded-md cursor-pointer">
                  Sign Out (Simulated)
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
