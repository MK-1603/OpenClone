"use client";

import React, { useState } from "react";
import {
  Settings,
  User,
  Palette,
  Bell,
  Shield,
  Save,
  CheckCircle2,
  Lock,
} from "lucide-react";
import { usePulse } from "@/context/PulseContext";

export const SettingsView: React.FC = () => {
  const { settings, updateSettings, team } = usePulse();
  const currentUser = team[0];

  const [workspaceName, setWorkspaceName] = useState(settings.workspaceName);
  const [theme, setTheme] = useState(settings.theme);
  const [emailNotifications, setEmailNotifications] = useState(settings.emailNotifications);
  const [desktopNotifications, setDesktopNotifications] = useState(settings.desktopNotifications);
  const [compactView, setCompactView] = useState(settings.compactView);
  const [savedSuccess, setSavedSuccess] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    updateSettings({
      workspaceName,
      theme,
      emailNotifications,
      desktopNotifications,
      compactView,
    });
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 3000);
  };

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Header */}
      <div className="p-4 rounded-xl bg-[#111111] border border-[rgba(255,255,255,0.07)] flex items-center justify-between">
        <div>
          <h2 className="text-sm font-semibold text-[#F5F5F5]">Workspace & System Preferences</h2>
          <p className="text-[11px] text-[#71717A]">
            Customize your command console appearance, notifications, and governance profile
          </p>
        </div>

        {savedSuccess && (
          <span className="flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-medium text-[#10B981] bg-[#064E3B] border border-[rgba(16,185,129,0.3)] animate-in fade-in">
            <CheckCircle2 className="w-3.5 h-3.5" />
            Preferences Saved
          </span>
        )}
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* Profile Card */}
        <div className="p-5 rounded-2xl bg-[#111111] border border-[rgba(255,255,255,0.08)] space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-[rgba(255,255,255,0.05)]">
            <User className="w-4 h-4 text-[#D6B36A]" />
            <h3 className="text-xs font-semibold text-[#F5F5F5]">User Profile</h3>
          </div>

          <div className="flex items-center gap-4">
            <img
              src={currentUser.avatar}
              alt={currentUser.name}
              className="w-14 h-14 rounded-full object-cover border-2 border-[rgba(214,179,106,0.5)]"
            />
            <div className="space-y-1">
              <h4 className="text-sm font-semibold text-[#F5F5F5]">{currentUser.name}</h4>
              <p className="text-xs text-[#A1A1AA]">{currentUser.role} · {currentUser.department}</p>
              <span className="text-[10px] text-[#71717A] font-mono">{currentUser.email}</span>
            </div>
          </div>
        </div>

        {/* Workspace Preferences */}
        <div className="p-5 rounded-2xl bg-[#111111] border border-[rgba(255,255,255,0.08)] space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-[rgba(255,255,255,0.05)]">
            <Shield className="w-4 h-4 text-[#D6B36A]" />
            <h3 className="text-xs font-semibold text-[#F5F5F5]">Workspace Settings</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-[#A1A1AA] mb-1">
                Workspace Name
              </label>
              <input
                type="text"
                value={workspaceName}
                onChange={(e) => setWorkspaceName(e.target.value)}
                className="w-full px-3 py-2 text-xs text-[#F5F5F5] bg-[#161616] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none focus:border-[rgba(214,179,106,0.5)]"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-[#A1A1AA] mb-1">
                Organization ID (Governed)
              </label>
              <div className="flex items-center justify-between px-3 py-2 text-xs text-[#71717A] bg-[#141414] border border-[rgba(255,255,255,0.06)] rounded-lg font-mono">
                <span>ORG-OPENCLONE-PULSE-2026</span>
                <Lock className="w-3.5 h-3.5 text-[#52525B]" />
              </div>
            </div>
          </div>
        </div>

        {/* Appearance & Design Tokens */}
        <div className="p-5 rounded-2xl bg-[#111111] border border-[rgba(255,255,255,0.08)] space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-[rgba(255,255,255,0.05)]">
            <Palette className="w-4 h-4 text-[#D6B36A]" />
            <h3 className="text-xs font-semibold text-[#F5F5F5]">Theme & Interface</h3>
          </div>

          <div className="space-y-3">
            <label className="block text-xs font-medium text-[#A1A1AA]">
              Base Color Theme
            </label>
            <div className="grid grid-cols-3 gap-3">
              {[
                { id: "charcoal", name: "Deep Charcoal (#0A0A0A)", preview: "#0A0A0A" },
                { id: "dark", name: "Midnight (#111111)", preview: "#111111" },
                { id: "oled", name: "Pure OLED (#000000)", preview: "#000000" },
              ].map((t) => (
                <div
                  key={t.id}
                  onClick={() => setTheme(t.id as any)}
                  className={`p-3 rounded-xl border cursor-pointer transition-all ${
                    theme === t.id
                      ? "bg-[#1C1C1E] border-[#D6B36A] shadow-[0_0_12px_rgba(214,179,106,0.15)]"
                      : "bg-[#141414] border-[rgba(255,255,255,0.06)] hover:border-[rgba(255,255,255,0.15)]"
                  }`}
                >
                  <div
                    className="w-full h-8 rounded-lg mb-2 border border-[rgba(255,255,255,0.1)]"
                    style={{ backgroundColor: t.preview }}
                  />
                  <span className="text-xs font-medium text-[#F5F5F5]">{t.name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Notification Preferences */}
        <div className="p-5 rounded-2xl bg-[#111111] border border-[rgba(255,255,255,0.08)] space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-[rgba(255,255,255,0.05)]">
            <Bell className="w-4 h-4 text-[#D6B36A]" />
            <h3 className="text-xs font-semibold text-[#F5F5F5]">Alerts & Notifications</h3>
          </div>

          <div className="space-y-3">
            <label className="flex items-center justify-between p-3 rounded-xl bg-[#141414] border border-[rgba(255,255,255,0.05)] cursor-pointer">
              <div>
                <span className="text-xs font-medium text-[#F5F5F5] block">
                  Critical Task Notifications
                </span>
                <span className="text-[11px] text-[#71717A]">
                  Receive immediate alerts when an urgent deliverable is updated
                </span>
              </div>
              <input
                type="checkbox"
                checked={desktopNotifications}
                onChange={(e) => setDesktopNotifications(e.target.checked)}
                className="w-4 h-4 accent-[#D6B36A] rounded"
              />
            </label>

            <label className="flex items-center justify-between p-3 rounded-xl bg-[#141414] border border-[rgba(255,255,255,0.05)] cursor-pointer">
              <div>
                <span className="text-xs font-medium text-[#F5F5F5] block">
                  Weekly Executive Digest Email
                </span>
                <span className="text-[11px] text-[#71717A]">
                  Summarize sprint velocity and milestone completion every Monday
                </span>
              </div>
              <input
                type="checkbox"
                checked={emailNotifications}
                onChange={(e) => setEmailNotifications(e.target.checked)}
                className="w-4 h-4 accent-[#D6B36A] rounded"
              />
            </label>
          </div>
        </div>

        {/* Submit Action */}
        <div className="flex justify-end pt-2">
          <button
            type="submit"
            className="flex items-center gap-2 px-5 py-2.5 text-xs font-semibold text-[#0E0E0E] bg-[#D6B36A] hover:bg-[#E0C58A] rounded-lg shadow-sm transition-all"
          >
            <Save className="w-3.5 h-3.5" />
            <span>Save Preferences</span>
          </button>
        </div>
      </form>
    </div>
  );
};
