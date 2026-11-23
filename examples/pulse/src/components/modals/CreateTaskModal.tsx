"use client";

import React, { useState } from "react";
import { X, CheckSquare } from "lucide-react";
import { usePulse } from "@/context/PulseContext";
import { TaskPriority, TaskStatus } from "@/types";

interface CreateTaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  defaultStatus?: TaskStatus;
}

export const CreateTaskModal: React.FC<CreateTaskModalProps> = ({
  isOpen,
  onClose,
  defaultStatus = "todo",
}) => {
  const { addTask, projects, team } = usePulse();

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [projectId, setProjectId] = useState(projects[0]?.id || "");
  const [assigneeId, setAssigneeId] = useState(team[0]?.id || "");
  const [priority, setPriority] = useState<TaskPriority>("medium");
  const [status, setStatus] = useState<TaskStatus>(defaultStatus);
  const [dueDate, setDueDate] = useState("2026-12-10");
  const [estimatedHours, setEstimatedHours] = useState(8);
  const [tagInput, setTagInput] = useState("Frontend, UX");

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    const project = projects.find((p) => p.id === projectId) || projects[0];
    const assignee = team.find((m) => m.id === assigneeId) || team[0];
    const tags = tagInput.split(",").map((t) => t.trim()).filter(Boolean);

    addTask({
      title: title.trim(),
      description: description.trim() || "No detailed description.",
      status,
      priority,
      projectId: project.id,
      projectName: project.name,
      assignee,
      dueDate,
      estimatedHours: Number(estimatedHours) || 8,
      tags: tags.length ? tags : ["General"],
    });

    setTitle("");
    setDescription("");
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div className="w-full max-w-lg bg-[#141414] border border-[rgba(255,255,255,0.12)] rounded-2xl shadow-2xl p-6 animate-in fade-in zoom-in-95 duration-150">
        <div className="flex items-center justify-between pb-4 border-b border-[rgba(255,255,255,0.06)]">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-[#222222] border border-[rgba(214,179,106,0.3)]">
              <CheckSquare className="w-4 h-4 text-[#D6B36A]" />
            </div>
            <div>
              <h2 className="text-sm font-semibold text-[#F5F5F5]">Create New Task</h2>
              <p className="text-[11px] text-[#71717A]">Add a deliverable to your project board</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1 rounded-md text-[#71717A] hover:text-[#F5F5F5] hover:bg-[#202020]">
            <X className="w-4 h-4" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="mt-4 space-y-3.5">
          <div>
            <label className="block text-xs font-medium text-[#A1A1AA] mb-1">Task Title *</label>
            <input
              type="text"
              required
              placeholder="e.g. Implement WebAuthn passkey registration"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-3 py-2 text-xs text-[#F5F5F5] bg-[#1A1A1A] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none focus:border-[rgba(214,179,106,0.5)]"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-[#A1A1AA] mb-1">Description</label>
            <textarea
              rows={3}
              placeholder="Detailed criteria, acceptance standards, and instructions..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-3 py-2 text-xs text-[#F5F5F5] bg-[#1A1A1A] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none focus:border-[rgba(214,179,106,0.5)] resize-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-[#A1A1AA] mb-1">Associated Project</label>
              <select
                value={projectId}
                onChange={(e) => setProjectId(e.target.value)}
                className="w-full px-3 py-2 text-xs text-[#F5F5F5] bg-[#1A1A1A] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none"
              >
                {projects.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-medium text-[#A1A1AA] mb-1">Assignee</label>
              <select
                value={assigneeId}
                onChange={(e) => setAssigneeId(e.target.value)}
                className="w-full px-3 py-2 text-xs text-[#F5F5F5] bg-[#1A1A1A] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none"
              >
                {team.map((m) => (
                  <option key={m.id} value={m.id}>
                    {m.name} ({m.role.split(" ")[0]})
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block text-xs font-medium text-[#A1A1AA] mb-1">Status Column</label>
              <select
                value={status}
                onChange={(e) => setStatus(e.target.value as TaskStatus)}
                className="w-full px-2.5 py-2 text-xs text-[#F5F5F5] bg-[#1A1A1A] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none"
              >
                <option value="backlog">Backlog</option>
                <option value="todo">Todo</option>
                <option value="in_progress">In Progress</option>
                <option value="review">Review</option>
                <option value="completed">Completed</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-medium text-[#A1A1AA] mb-1">Priority</label>
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value as TaskPriority)}
                className="w-full px-2.5 py-2 text-xs text-[#F5F5F5] bg-[#1A1A1A] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-medium text-[#A1A1AA] mb-1">Due Date</label>
              <input
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                className="w-full px-2.5 py-2 text-xs text-[#F5F5F5] bg-[#1A1A1A] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-[#A1A1AA] mb-1">Tags (comma-separated)</label>
            <input
              type="text"
              placeholder="e.g. Frontend, Auth, Security"
              value={tagInput}
              onChange={(e) => setTagInput(e.target.value)}
              className="w-full px-3 py-2 text-xs text-[#F5F5F5] bg-[#1A1A1A] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none"
            />
          </div>

          <div className="flex items-center justify-end gap-3 pt-4 border-t border-[rgba(255,255,255,0.06)]">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-medium text-[#A1A1AA] hover:text-[#F5F5F5] bg-[#1A1A1A] hover:bg-[#222222] rounded-lg transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-xs font-semibold text-[#0E0E0E] bg-[#D6B36A] hover:bg-[#E0C58A] rounded-lg shadow-sm transition-all"
            >
              Add Task
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
