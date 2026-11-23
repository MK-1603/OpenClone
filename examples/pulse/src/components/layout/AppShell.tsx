"use client";

import React, { useState } from "react";
import { Sidebar, NavItemKey } from "./Sidebar";
import { Header } from "./Header";
import { usePulse } from "@/context/PulseContext";
import { DashboardView } from "../views/DashboardView";
import { ProjectsView } from "../views/ProjectsView";
import { TasksView } from "../views/TasksView";
import { CalendarView } from "../views/CalendarView";
import { AnalyticsView } from "../views/AnalyticsView";
import { TeamView } from "../views/TeamView";
import { ActivityView } from "../views/ActivityView";
import { SettingsView } from "../views/SettingsView";
import { QuickCreateModal } from "../modals/QuickCreateModal";

export const AppShell: React.FC = () => {
  const [activeTab, setActiveTab] = useState<NavItemKey>("dashboard");
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const { quickCreateOpen, setQuickCreateOpen } = usePulse();

  const renderActiveView = () => {
    switch (activeTab) {
      case "dashboard":
        return <DashboardView onNavigate={(tab) => setActiveTab(tab)} />;
      case "projects":
        return <ProjectsView />;
      case "tasks":
        return <TasksView />;
      case "calendar":
        return <CalendarView />;
      case "analytics":
        return <AnalyticsView />;
      case "team":
        return <TeamView />;
      case "activity":
        return <ActivityView />;
      case "settings":
        return <SettingsView />;
      default:
        return <DashboardView onNavigate={(tab) => setActiveTab(tab)} />;
    }
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#0A0A0A] text-[#F5F5F5]">
      {/* Sidebar */}
      <Sidebar
        activeTab={activeTab}
        onTabChange={(tab) => setActiveTab(tab)}
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
      />

      {/* Main Content Area */}
      <div className="flex flex-col flex-1 h-screen overflow-hidden">
        {/* Header */}
        <Header
          currentTab={activeTab}
          onOpenQuickCreate={() => setQuickCreateOpen(true)}
        />

        {/* Dynamic Page Container */}
        <main className="flex-1 overflow-y-auto px-6 py-6 scroll-smooth">
          <div className="max-w-7xl mx-auto">{renderActiveView()}</div>
        </main>
      </div>

      {/* Quick Create Dialog */}
      <QuickCreateModal
        isOpen={quickCreateOpen}
        onClose={() => setQuickCreateOpen(false)}
      />
    </div>
  );
};
