"use client";

import React, { useState } from "react";
import {
  LayoutDashboard,
  FolderKanban,
  CheckSquare,
  Calendar,
  BarChart3,
  Users,
  Activity as ActivityIcon,
  Settings,
  ChevronLeft,
  ChevronRight,
  ShieldCheck,
  ChevronDown,
} from "lucide-react";

export type NavItemKey =
  | "dashboard"
  | "projects"
  | "tasks"
  | "calendar"
  | "analytics"
  | "team"
  | "activity"
  | "settings";

interface SidebarProps {
  activeTab: NavItemKey;
  onTabChange: (tab: NavItemKey) => void;
  collapsed: boolean;
  onToggleCollapse: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  onTabChange,
  collapsed,
  onToggleCollapse,
}) => {
  const [workspaceMenuOpen, setWorkspaceMenuOpen] = useState(false);
  const [activeWorkspace, setActiveWorkspace] = useState("Aether Labs Global");

  const workspaces = ["Aether Labs Global", "Pulse Engineering", "Personal Workspace"];

  const navItems: { key: NavItemKey; label: string; icon: React.ReactNode; badge?: string }[] = [
    { key: "dashboard", label: "Dashboard", icon: <LayoutDashboard className="w-4 h-4" /> },
    { key: "projects", label: "Projects", icon: <FolderKanban className="w-4 h-4" />, badge: "6" },
    { key: "tasks", label: "Tasks", icon: <CheckSquare className="w-4 h-4" />, badge: "10" },
    { key: "calendar", label: "Calendar", icon: <Calendar className="w-4 h-4" /> },
    { key: "analytics", label: "Analytics", icon: <BarChart3 className="w-4 h-4" /> },
    { key: "team", label: "Team", icon: <Users className="w-4 h-4" /> },
    { key: "activity", label: "Activity", icon: <ActivityIcon className="w-4 h-4" /> },
    { key: "settings", label: "Settings", icon: <Settings className="w-4 h-4" /> },
  ];

  return (
    <aside
      className={`relative flex flex-col h-screen bg-[#0E0E0E] border-r border-[rgba(255,255,255,0.08)] transition-all duration-300 select-none z-30 ${
        collapsed ? "w-20" : "w-64"
      }`}
    >
      {/* Brand Header */}
      <div className="flex items-center justify-between h-16 px-4 border-b border-[rgba(255,255,255,0.06)]">
        <div className="flex items-center gap-3 overflow-hidden cursor-pointer" onClick={() => onTabChange("dashboard")}>
          <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-gradient-to-br from-[#181818] to-[#121212] border border-[rgba(214,179,106,0.35)] shadow-sm">
            <div className="w-3.5 h-3.5 rounded-sm bg-[#D6B36A] shadow-[0_0_10px_rgba(214,179,106,0.5)]" />
          </div>
          {!collapsed && (
            <div className="flex flex-col">
              <span className="font-semibold tracking-wider text-sm text-[#F5F5F5] uppercase">
                PULSE
              </span>
              <span className="text-[10px] text-[#71717A] tracking-tight">Command Center</span>
            </div>
          )}
        </div>

        <button
          onClick={onToggleCollapse}
          className="p-1 rounded-md text-[#71717A] hover:text-[#F5F5F5] hover:bg-[#181818] transition-colors"
          title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {/* Workspace Selector */}
      {!collapsed ? (
        <div className="relative px-3 py-3 border-b border-[rgba(255,255,255,0.05)]">
          <button
            onClick={() => setWorkspaceMenuOpen(!workspaceMenuOpen)}
            className="flex items-center justify-between w-full px-2.5 py-1.5 text-xs text-[#A1A1AA] bg-[#141414] hover:bg-[#1A1A1A] hover:text-[#F5F5F5] border border-[rgba(255,255,255,0.06)] rounded-md transition-colors"
          >
            <div className="flex items-center gap-2 truncate">
              <div className="w-2 h-2 rounded-full bg-[#10B981]" />
              <span className="truncate font-medium">{activeWorkspace}</span>
            </div>
            <ChevronDown className="w-3.5 h-3.5 text-[#71717A]" />
          </button>

          {workspaceMenuOpen && (
            <div className="absolute top-12 left-3 right-3 bg-[#181818] border border-[rgba(255,255,255,0.12)] rounded-md shadow-xl py-1 z-40">
              {workspaces.map((ws) => (
                <div
                  key={ws}
                  onClick={() => {
                    setActiveWorkspace(ws);
                    setWorkspaceMenuOpen(false);
                  }}
                  className={`px-3 py-1.5 text-xs cursor-pointer hover:bg-[#222222] ${
                    ws === activeWorkspace ? "text-[#D6B36A] font-semibold" : "text-[#A1A1AA]"
                  }`}
                >
                  {ws}
                </div>
              ))}
            </div>
          )}
        </div>
      ) : (
        <div className="flex justify-center py-3 border-b border-[rgba(255,255,255,0.05)]">
          <div className="w-2 h-2 rounded-full bg-[#10B981]" title={activeWorkspace} />
        </div>
      )}

      {/* Navigation List */}
      <nav className="flex-1 px-2.5 py-4 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const isActive = activeTab === item.key;
          return (
            <button
              key={item.key}
              onClick={() => onTabChange(item.key)}
              title={collapsed ? item.label : undefined}
              className={`flex items-center w-full px-3 py-2 rounded-lg text-xs font-medium transition-all ${
                isActive
                  ? "bg-[#181818] text-[#D6B36A] border border-[rgba(214,179,106,0.25)] shadow-[0_2px_10px_rgba(0,0,0,0.4)]"
                  : "text-[#A1A1AA] hover:text-[#F5F5F5] hover:bg-[#141414] border border-transparent"
              } ${collapsed ? "justify-center" : "justify-between"}`}
            >
              <div className="flex items-center gap-3">
                <span className={isActive ? "text-[#D6B36A]" : "text-[#71717A]"}>
                  {item.icon}
                </span>
                {!collapsed && <span>{item.label}</span>}
              </div>

              {!collapsed && item.badge && (
                <span
                  className={`px-1.5 py-0.5 text-[10px] font-semibold rounded-full ${
                    isActive
                      ? "bg-[#252014] text-[#D6B36A] border border-[rgba(214,179,106,0.3)]"
                      : "bg-[#1C1C1E] text-[#71717A]"
                  }`}
                >
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Footer Governance Status */}
      <div className="p-3 border-t border-[rgba(255,255,255,0.06)] bg-[#0A0A0A]">
        {!collapsed ? (
          <div className="flex items-center gap-2 p-2 rounded-lg bg-[#121212] border border-[rgba(255,255,255,0.06)]">
            <ShieldCheck className="w-4 h-4 text-[#D6B36A] shrink-0" />
            <div className="flex flex-col min-w-0">
              <span className="text-[11px] font-medium text-[#F5F5F5] truncate">OpenClone v2.0</span>
              <span className="text-[9px] text-[#71717A] truncate">Governed Engine Active</span>
            </div>
          </div>
        ) : (
          <div className="flex justify-center p-1" title="OpenClone Governed Runtime">
            <ShieldCheck className="w-4 h-4 text-[#D6B36A]" />
          </div>
        )}
      </div>
    </aside>
  );
};
