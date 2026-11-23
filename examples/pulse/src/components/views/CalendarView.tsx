"use client";

import React, { useState } from "react";
import {
  ChevronLeft,
  ChevronRight,
  Calendar as CalendarIcon,
  Clock,
  Tag,
  AlertCircle,
  Plus,
} from "lucide-react";
import { usePulse } from "@/context/PulseContext";

export const CalendarView: React.FC = () => {
  const { tasks, projects } = usePulse();
  const [currentMonth, setCurrentMonth] = useState("November 2026");
  const [viewMode, setViewMode] = useState<"month" | "week">("month");
  const [selectedDay, setSelectedDay] = useState<number | null>(23);

  // Generate 30 days for November 2026 (Starts on a Sunday, Nov 1 = Sun)
  const daysInMonth = Array.from({ length: 30 }, (_, i) => i + 1);

  // Days of week
  const weekDays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

  // Map tasks to days (e.g. November 2026)
  const getTasksForDay = (day: number) => {
    const dateStr = `2026-11-${String(day).padStart(2, "0")}`;
    return tasks.filter((t) => t.dueDate === dateStr);
  };

  const selectedDayTasks = selectedDay ? getTasksForDay(selectedDay) : [];

  return (
    <div className="space-y-6">
      {/* Calendar Header Navigation */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-4 rounded-xl bg-[#111111] border border-[rgba(255,255,255,0.07)]">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1 bg-[#161616] border border-[rgba(255,255,255,0.08)] rounded-lg p-1">
            <button
              onClick={() => setCurrentMonth("October 2026")}
              className="p-1 rounded text-[#71717A] hover:text-[#F5F5F5]"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="px-3 text-xs font-semibold text-[#F5F5F5] min-w-[120px] text-center">
              {currentMonth}
            </span>
            <button
              onClick={() => setCurrentMonth("December 2026")}
              className="p-1 rounded text-[#71717A] hover:text-[#F5F5F5]"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          <button
            onClick={() => setSelectedDay(23)}
            className="px-3 py-1.5 text-xs text-[#A1A1AA] hover:text-[#F5F5F5] bg-[#161616] border border-[rgba(255,255,255,0.08)] rounded-lg"
          >
            Today
          </button>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex items-center p-1 bg-[#161616] border border-[rgba(255,255,255,0.08)] rounded-lg text-xs">
            <button
              onClick={() => setViewMode("month")}
              className={`px-3 py-1 rounded-md font-medium ${
                viewMode === "month" ? "bg-[#252525] text-[#D6B36A]" : "text-[#71717A]"
              }`}
            >
              Month View
            </button>
            <button
              onClick={() => setViewMode("week")}
              className={`px-3 py-1 rounded-md font-medium ${
                viewMode === "week" ? "bg-[#252525] text-[#D6B36A]" : "text-[#71717A]"
              }`}
            >
              Week View
            </button>
          </div>
        </div>
      </div>

      {/* Main Calendar Grid and Event Details Sidebar */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">
        {/* Month Grid */}
        <div className="lg:col-span-3 rounded-2xl bg-[#111111] border border-[rgba(255,255,255,0.08)] p-5 overflow-hidden">
          {/* Weekday headers */}
          <div className="grid grid-cols-7 gap-2 pb-3 mb-2 border-b border-[rgba(255,255,255,0.06)] text-center text-xs font-medium text-[#71717A]">
            {weekDays.map((wd) => (
              <div key={wd}>{wd}</div>
            ))}
          </div>

          {/* Days Grid */}
          <div className="grid grid-cols-7 gap-2">
            {daysInMonth.map((day) => {
              const dayTasks = getTasksForDay(day);
              const isSelected = selectedDay === day;
              const isToday = day === 23;

              return (
                <div
                  key={day}
                  onClick={() => setSelectedDay(day)}
                  className={`min-h-[92px] p-2 rounded-xl border transition-all cursor-pointer flex flex-col justify-between ${
                    isSelected
                      ? "bg-[#1A1A1A] border-[#D6B36A] shadow-[0_0_15px_rgba(214,179,106,0.15)]"
                      : "bg-[#141414] border-[rgba(255,255,255,0.05)] hover:border-[rgba(255,255,255,0.15)]"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span
                      className={`text-xs font-mono font-medium ${
                        isToday
                          ? "w-5 h-5 rounded-full bg-[#D6B36A] text-[#0E0E0E] flex items-center justify-center font-bold"
                          : "text-[#A1A1AA]"
                      }`}
                    >
                      {day}
                    </span>
                    {dayTasks.length > 0 && (
                      <span className="w-1.5 h-1.5 rounded-full bg-[#D6B36A]" />
                    )}
                  </div>

                  <div className="space-y-1 mt-1">
                    {dayTasks.slice(0, 2).map((t) => (
                      <div
                        key={t.id}
                        className="px-1.5 py-0.5 rounded text-[9px] font-medium bg-[#1C1C1E] text-[#D6B36A] border border-[rgba(214,179,106,0.2)] truncate"
                        title={t.title}
                      >
                        {t.title}
                      </div>
                    ))}
                    {dayTasks.length > 2 && (
                      <span className="text-[9px] text-[#71717A] pl-1 font-mono">
                        +{dayTasks.length - 2} more
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Selected Day Agenda & Upcoming Deadlines */}
        <div className="rounded-2xl bg-[#111111] border border-[rgba(255,255,255,0.08)] p-5 space-y-5">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-[rgba(255,255,255,0.06)]">
              <h3 className="text-xs font-semibold text-[#F5F5F5]">
                {selectedDay ? `Agenda for Nov ${selectedDay}, 2026` : "Select a date"}
              </h3>
              <span className="text-[10px] text-[#D6B36A]">
                {selectedDayTasks.length} Scheduled
              </span>
            </div>

            <div className="mt-3 space-y-2.5">
              {selectedDayTasks.length > 0 ? (
                selectedDayTasks.map((task) => (
                  <div
                    key={task.id}
                    className="p-3 rounded-xl bg-[#161616] border border-[rgba(255,255,255,0.06)]"
                  >
                    <div className="flex items-center justify-between text-[10px] text-[#71717A]">
                      <span>{task.projectName}</span>
                      <span className="font-semibold text-[#D6B36A]">{task.priority}</span>
                    </div>
                    <h4 className="mt-1 text-xs font-semibold text-[#F5F5F5]">{task.title}</h4>
                    <p className="mt-0.5 text-[11px] text-[#A1A1AA] line-clamp-2">
                      {task.description}
                    </p>
                    <div className="mt-2 flex items-center justify-between text-[10px] text-[#71717A]">
                      <div className="flex items-center gap-1.5">
                        <img
                          src={task.assignee.avatar}
                          alt={task.assignee.name}
                          className="w-4 h-4 rounded-full object-cover"
                        />
                        <span>{task.assignee.name.split(" ")[0]}</span>
                      </div>
                      <span className="capitalize">{task.status.replace("_", " ")}</span>
                    </div>
                  </div>
                ))
              ) : (
                <div className="py-8 text-center border border-dashed border-[rgba(255,255,255,0.05)] rounded-xl">
                  <CalendarIcon className="w-6 h-6 text-[#52525B] mx-auto mb-1.5" />
                  <p className="text-xs text-[#71717A]">No deliverables due on this date</p>
                </div>
              )}
            </div>
          </div>

          {/* Upcoming Project Milestones */}
          <div className="pt-3 border-t border-[rgba(255,255,255,0.06)]">
            <h4 className="text-xs font-semibold text-[#F5F5F5] mb-2.5">Upcoming Milestones</h4>
            <div className="space-y-2">
              {projects.slice(0, 3).map((p) => (
                <div
                  key={p.id}
                  className="p-2.5 rounded-lg bg-[#141414] border border-[rgba(255,255,255,0.04)] text-xs"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-[#F5F5F5] truncate max-w-[130px]">
                      {p.name}
                    </span>
                    <span className="text-[10px] text-[#D6B36A] font-mono">{p.dueDate}</span>
                  </div>
                  <div className="text-[10px] text-[#71717A] mt-1">Lead: {p.owner.name}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
