"use client";

import React, { useState } from "react";
import { X, FolderPlus } from "lucide-react";
import { usePulse } from "@/context/PulseContext";
import { ProjectPriority } from "@/types";

interface CreateProjectModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const CreateProjectModal: React.FC<CreateProjectModalProps> = ({ isOpen, onClose }) => {
  const { addProject, team } = usePulse();

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("Core Architecture");
  const [priority, setPriority] = useState<ProjectPriority>("high");
  const [ownerId, setOwnerId] = useState(team[0]?.id || "");
  const [budget, setBudget] = useState("$50,000");
  const [dueDate, setDueDate] = useState("2027-01-31");

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;

    const owner = team.find((m) => m.id === ownerId) || team[0];

    addProject({
      name: name.trim(),
      description: description.trim() || "No description provided.",
      status: "in_progress",
      priority,
      category,
      owner,
      team: [owner],
      startDate: new Date().toISOString().split("T")[0],
      dueDate,
      budget,
      health: "healthy",
    });

    setName("");
    setDescription("");
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div className="w-full max-w-lg bg-[#141414] border border-[rgba(255,255,255,0.12)] rounded-2xl shadow-2xl p-6 animate-in fade-in zoom-in-95 duration-150">
        <div className="flex items-center justify-between pb-4 border-b border-[rgba(255,255,255,0.06)]">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-[#222222] border border-[rgba(214,179,106,0.3)]">
              <FolderPlus className="w-4 h-4 text-[#D6B36A]" />
            </div>
            <div>
              <h2 className="text-sm font-semibold text-[#F5F5F5]">Create New Project</h2>
              <p className="text-[11px] text-[#71717A]">Initialize a project workspace in PULSE</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1 rounded-md text-[#71717A] hover:text-[#F5F5F5] hover:bg-[#202020]">
            <X className="w-4 h-4" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="mt-4 space-y-3.5">
          <div>
            <label className="block text-xs font-medium text-[#A1A1AA] mb-1">Project Name *</label>
            <input
              type="text"
              required
              placeholder="e.g. Aether Engine v3.0"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-3 py-2 text-xs text-[#F5F5F5] bg-[#1A1A1A] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none focus:border-[rgba(214,179,106,0.5)]"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-[#A1A1AA] mb-1">Description</label>
            <textarea
              rows={3}
              placeholder="Summary of project goals, technical constraints, and deliverables..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-3 py-2 text-xs text-[#F5F5F5] bg-[#1A1A1A] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none focus:border-[rgba(214,179,106,0.5)] resize-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-[#A1A1AA] mb-1">Category</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-3 py-2 text-xs text-[#F5F5F5] bg-[#1A1A1A] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none"
              >
                <option value="Core Architecture">Core Architecture</option>
                <option value="AI Infrastructure">AI Infrastructure</option>
                <option value="Mobile">Mobile</option>
                <option value="Security & Compliance">Security & Compliance</option>
                <option value="Design">Design</option>
                <option value="Infrastructure">Infrastructure</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-medium text-[#A1A1AA] mb-1">Priority</label>
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value as ProjectPriority)}
                className="w-full px-3 py-2 text-xs text-[#F5F5F5] bg-[#1A1A1A] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block text-xs font-medium text-[#A1A1AA] mb-1">Project Lead</label>
              <select
                value={ownerId}
                onChange={(e) => setOwnerId(e.target.value)}
                className="w-full px-2.5 py-2 text-xs text-[#F5F5F5] bg-[#1A1A1A] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none"
              >
                {team.map((m) => (
                  <option key={m.id} value={m.id}>
                    {m.name.split(" ")[0]} ({m.role.split(" ")[0]})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-medium text-[#A1A1AA] mb-1">Target Due Date</label>
              <input
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                className="w-full px-2.5 py-2 text-xs text-[#F5F5F5] bg-[#1A1A1A] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-[#A1A1AA] mb-1">Allocated Budget</label>
              <input
                type="text"
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
                className="w-full px-2.5 py-2 text-xs text-[#F5F5F5] bg-[#1A1A1A] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none"
              />
            </div>
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
              Create Project
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
