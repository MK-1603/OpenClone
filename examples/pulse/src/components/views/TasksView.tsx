"use client";

import React, { useState } from "react";
import {
  CheckSquare,
  Plus,
  Search,
  Filter,
  Columns3,
  List as ListIcon,
  Clock,
  Trash2,
  ChevronRight,
  ChevronLeft,
  Calendar,
  AlertCircle,
  Tag,
} from "lucide-react";
import { usePulse } from "@/context/PulseContext";
import { Task, TaskPriority, TaskStatus } from "@/types";
import { CreateTaskModal } from "../modals/CreateTaskModal";
import { ConfirmDeleteModal } from "../modals/ConfirmDeleteModal";

const KANBAN_COLUMNS: { key: TaskStatus; label: string; color: string }[] = [
  { key: "backlog", label: "Backlog", color: "#71717A" },
  { key: "todo", label: "Todo", color: "#3B82F6" },
  { key: "in_progress", label: "In Progress", color: "#D6B36A" },
  { key: "review", label: "Review", color: "#A855F7" },
  { key: "completed", label: "Completed", color: "#10B981" },
];

export const TasksView: React.FC = () => {
  const { tasks, updateTaskStatus, deleteTask, projects, searchQuery, setSearchQuery } = usePulse();
  const [viewMode, setViewMode] = useState<"kanban" | "list">("kanban");
  const [projectFilter, setProjectFilter] = useState<string>("all");
  const [priorityFilter, setPriorityFilter] = useState<string>("all");

  const [createModalOpen, setCreateModalOpen] = useState(false);
  const [targetColumnStatus, setTargetColumnStatus] = useState<TaskStatus>("todo");

  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [selectedTaskId, setSelectedTaskId] = useState<string | null>(null);

  // Filters
  const filteredTasks = tasks.filter((t) => {
    const matchesSearch =
      t.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.tags.some((tag) => tag.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesProject = projectFilter === "all" || t.projectId === projectFilter;
    const matchesPriority = priorityFilter === "all" || t.priority === priorityFilter;
    return matchesSearch && matchesProject && matchesPriority;
  });

  const handleOpenCreateForColumn = (status: TaskStatus) => {
    setTargetColumnStatus(status);
    setCreateModalOpen(true);
  };

  const handleDeleteTask = (id: string) => {
    setSelectedTaskId(id);
    setDeleteModalOpen(true);
  };

  // Move task to next or previous status in Kanban
  const moveTask = (taskId: string, direction: "prev" | "next") => {
    const task = tasks.find((t) => t.id === taskId);
    if (!task) return;
    const colOrder: TaskStatus[] = ["backlog", "todo", "in_progress", "review", "completed"];
    const currentIndex = colOrder.indexOf(task.status);
    if (direction === "next" && currentIndex < colOrder.length - 1) {
      updateTaskStatus(taskId, colOrder[currentIndex + 1]);
    } else if (direction === "prev" && currentIndex > 0) {
      updateTaskStatus(taskId, colOrder[currentIndex - 1]);
    }
  };

  return (
    <div className="space-y-6">
      {/* Task Filters & Action Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-4 rounded-xl bg-[#111111] border border-[rgba(255,255,255,0.07)]">
        <div className="flex items-center gap-3 flex-wrap flex-1">
          {/* Search */}
          <div className="relative min-w-[220px]">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#71717A]" />
            <input
              type="text"
              placeholder="Search tasks, tags..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 text-xs text-[#F5F5F5] bg-[#161616] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none focus:border-[rgba(214,179,106,0.5)] placeholder-[#52525B]"
            />
          </div>

          {/* Project Filter */}
          <select
            value={projectFilter}
            onChange={(e) => setProjectFilter(e.target.value)}
            className="px-2.5 py-1.5 text-xs text-[#A1A1AA] bg-[#161616] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none"
          >
            <option value="all">All Projects</option>
            {projects.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name}
              </option>
            ))}
          </select>

          {/* Priority Filter */}
          <select
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
            className="px-2.5 py-1.5 text-xs text-[#A1A1AA] bg-[#161616] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none"
          >
            <option value="all">All Priorities</option>
            <option value="urgent">Urgent</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>

        <div className="flex items-center gap-2">
          {/* View Toggle */}
          <div className="flex items-center p-1 bg-[#161616] border border-[rgba(255,255,255,0.08)] rounded-lg">
            <button
              onClick={() => setViewMode("kanban")}
              className={`p-1.5 rounded-md ${
                viewMode === "kanban" ? "bg-[#252525] text-[#D6B36A]" : "text-[#71717A]"
              }`}
              title="Kanban Board"
            >
              <Columns3 className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => setViewMode("list")}
              className={`p-1.5 rounded-md ${
                viewMode === "list" ? "bg-[#252525] text-[#D6B36A]" : "text-[#71717A]"
              }`}
              title="List View"
            >
              <ListIcon className="w-3.5 h-3.5" />
            </button>
          </div>

          <button
            onClick={() => handleOpenCreateForColumn("todo")}
            className="flex items-center gap-1.5 px-3.5 py-1.5 text-xs font-semibold text-[#0E0E0E] bg-[#D6B36A] hover:bg-[#E0C58A] rounded-lg shadow-sm transition-all"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>New Task</span>
          </button>
        </div>
      </div>

      {/* Kanban Board View */}
      {viewMode === "kanban" ? (
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4 items-start overflow-x-auto pb-4">
          {KANBAN_COLUMNS.map((col) => {
            const colTasks = filteredTasks.filter((t) => t.status === col.key);
            return (
              <div
                key={col.key}
                className="flex flex-col min-w-[240px] bg-[#0E0E0E] border border-[rgba(255,255,255,0.06)] rounded-2xl p-3"
              >
                {/* Column Header */}
                <div className="flex items-center justify-between pb-3 mb-3 border-b border-[rgba(255,255,255,0.04)]">
                  <div className="flex items-center gap-2">
                    <span
                      className="w-2 h-2 rounded-full"
                      style={{ backgroundColor: col.color }}
                    />
                    <h3 className="text-xs font-semibold text-[#F5F5F5]">{col.label}</h3>
                    <span className="px-1.5 py-0.2 text-[10px] font-mono text-[#71717A] bg-[#161616] rounded">
                      {colTasks.length}
                    </span>
                  </div>

                  <button
                    onClick={() => handleOpenCreateForColumn(col.key)}
                    className="p-1 rounded text-[#71717A] hover:text-[#D6B36A] hover:bg-[#181818]"
                    title={`Add task to ${col.label}`}
                  >
                    <Plus className="w-3.5 h-3.5" />
                  </button>
                </div>

                {/* Column Task Cards */}
                <div className="space-y-3 min-h-[140px]">
                  {colTasks.map((task) => (
                    <div
                      key={task.id}
                      className="p-3.5 rounded-xl bg-[#141414] hover:bg-[#171717] border border-[rgba(255,255,255,0.06)] hover:border-[rgba(214,179,106,0.3)] transition-all group shadow-sm"
                    >
                      {/* Priority & Delete */}
                      <div className="flex items-center justify-between mb-2">
                        <span
                          className={`px-1.5 py-0.5 text-[9px] font-semibold rounded uppercase ${
                            task.priority === "urgent"
                              ? "bg-[#281515] text-[#EF4444]"
                              : task.priority === "high"
                              ? "bg-[#2C1D0E] text-[#F59E0B]"
                              : "bg-[#112233] text-[#60A5FA]"
                          }`}
                        >
                          {task.priority}
                        </span>

                        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button
                            onClick={() => moveTask(task.id, "prev")}
                            className="p-0.5 text-[#71717A] hover:text-[#F5F5F5]"
                            title="Move left"
                          >
                            <ChevronLeft className="w-3 h-3" />
                          </button>
                          <button
                            onClick={() => moveTask(task.id, "next")}
                            className="p-0.5 text-[#71717A] hover:text-[#F5F5F5]"
                            title="Move right"
                          >
                            <ChevronRight className="w-3 h-3" />
                          </button>
                          <button
                            onClick={() => handleDeleteTask(task.id)}
                            className="p-0.5 text-[#71717A] hover:text-[#EF4444]"
                            title="Delete"
                          >
                            <Trash2 className="w-3 h-3" />
                          </button>
                        </div>
                      </div>

                      {/* Title & Project */}
                      <h4 className="text-xs font-semibold text-[#F5F5F5] group-hover:text-[#D6B36A] transition-colors leading-snug">
                        {task.title}
                      </h4>
                      <p className="mt-1 text-[11px] text-[#71717A] line-clamp-2 leading-relaxed">
                        {task.description}
                      </p>

                      {/* Tags */}
                      <div className="mt-2.5 flex flex-wrap gap-1">
                        {task.tags.map((tag) => (
                          <span
                            key={tag}
                            className="px-1.5 py-0.5 text-[9px] rounded bg-[#1B1B1B] text-[#A1A1AA]"
                          >
                            #{tag}
                          </span>
                        ))}
                      </div>

                      {/* Footer Meta */}
                      <div className="mt-3 pt-2.5 border-t border-[rgba(255,255,255,0.04)] flex items-center justify-between text-[10px] text-[#71717A]">
                        <span className="truncate max-w-[110px]" title={task.projectName}>
                          {task.projectName}
                        </span>
                        <div className="flex items-center gap-1.5">
                          <img
                            src={task.assignee.avatar}
                            alt={task.assignee.name}
                            className="w-4 h-4 rounded-full object-cover"
                            title={`Assigned to ${task.assignee.name}`}
                          />
                        </div>
                      </div>
                    </div>
                  ))}

                  {colTasks.length === 0 && (
                    <div className="flex items-center justify-center h-28 border border-dashed border-[rgba(255,255,255,0.06)] rounded-xl text-center p-3">
                      <span className="text-[11px] text-[#52525B]">No tasks in {col.label}</span>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        /* List View */
        <div className="overflow-x-auto rounded-2xl bg-[#111111] border border-[rgba(255,255,255,0.08)]">
          <table className="w-full text-left text-xs text-[#A1A1AA]">
            <thead className="bg-[#141414] text-[11px] text-[#71717A] uppercase border-b border-[rgba(255,255,255,0.06)]">
              <tr>
                <th className="px-5 py-3 font-semibold">Deliverable</th>
                <th className="px-4 py-3 font-semibold">Project</th>
                <th className="px-4 py-3 font-semibold">Status</th>
                <th className="px-4 py-3 font-semibold">Priority</th>
                <th className="px-4 py-3 font-semibold">Assignee</th>
                <th className="px-4 py-3 font-semibold">Due Date</th>
                <th className="px-4 py-3 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[rgba(255,255,255,0.04)]">
              {filteredTasks.map((task) => (
                <tr key={task.id} className="hover:bg-[#161616] transition-colors">
                  <td className="px-5 py-3 font-medium text-[#F5F5F5]">{task.title}</td>
                  <td className="px-4 py-3 text-[#A1A1AA]">{task.projectName}</td>
                  <td className="px-4 py-3">
                    <span className="px-2 py-0.5 text-[10px] font-semibold rounded bg-[#1A1A1A] text-[#D6B36A] uppercase">
                      {task.status.replace("_", " ")}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <span
                      className={`text-[10px] font-semibold uppercase ${
                        task.priority === "urgent" ? "text-[#EF4444]" : "text-[#F59E0B]"
                      }`}
                    >
                      {task.priority}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-1.5">
                      <img
                        src={task.assignee.avatar}
                        alt={task.assignee.name}
                        className="w-4 h-4 rounded-full object-cover"
                      />
                      <span>{task.assignee.name}</span>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-[11px] text-[#71717A]">{task.dueDate}</td>
                  <td className="px-4 py-3 text-right">
                    <button
                      onClick={() => handleDeleteTask(task.id)}
                      className="p-1 rounded text-[#71717A] hover:text-[#EF4444]"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Modals */}
      <CreateTaskModal
        isOpen={createModalOpen}
        onClose={() => setCreateModalOpen(false)}
        defaultStatus={targetColumnStatus}
      />

      <ConfirmDeleteModal
        isOpen={deleteModalOpen}
        onClose={() => setDeleteModalOpen(false)}
        onConfirm={() => selectedTaskId && deleteTask(selectedTaskId)}
        title="Delete Deliverable"
        message="Are you sure you want to delete this task? This action will permanently remove it from your project sprint board."
      />
    </div>
  );
};
