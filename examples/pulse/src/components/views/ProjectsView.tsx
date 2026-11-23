"use client";

import React, { useState } from "react";
import {
  FolderPlus,
  LayoutGrid,
  List as ListIcon,
  Search,
  Filter,
  Calendar,
  MoreVertical,
  Trash2,
  ExternalLink,
  Users,
  CheckCircle,
} from "lucide-react";
import { usePulse } from "@/context/PulseContext";
import { Project, ProjectStatus } from "@/types";
import { CreateProjectModal } from "../modals/CreateProjectModal";
import { ConfirmDeleteModal } from "../modals/ConfirmDeleteModal";

export const ProjectsView: React.FC = () => {
  const { projects, deleteProject, searchQuery, setSearchQuery } = usePulse();
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [categoryFilter, setCategoryFilter] = useState<string>("all");
  const [sortBy, setSortBy] = useState<"name" | "progress" | "dueDate">("progress");

  const [createModalOpen, setCreateModalOpen] = useState(false);
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [selectedProjectId, setSelectedProjectId] = useState<string | null>(null);

  // Filter & Search
  const filtered = projects.filter((p) => {
    const matchesSearch =
      p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.category.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === "all" || p.status === statusFilter;
    const matchesCategory = categoryFilter === "all" || p.category === categoryFilter;
    return matchesSearch && matchesStatus && matchesCategory;
  });

  // Sort
  const sorted = [...filtered].sort((a, b) => {
    if (sortBy === "name") return a.name.localeCompare(b.name);
    if (sortBy === "progress") return b.progress - a.progress;
    if (sortBy === "dueDate") return new Date(a.dueDate).getTime() - new Date(b.dueDate).getTime();
    return 0;
  });

  const categories = Array.from(new Set(projects.map((p) => p.category)));

  const handleDelete = (id: string) => {
    setSelectedProjectId(id);
    setDeleteModalOpen(true);
  };

  return (
    <div className="space-y-6">
      {/* Controls & Filter Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-4 rounded-xl bg-[#111111] border border-[rgba(255,255,255,0.07)]">
        <div className="flex items-center gap-3 flex-wrap flex-1">
          {/* Search */}
          <div className="relative min-w-[220px]">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#71717A]" />
            <input
              type="text"
              placeholder="Search projects..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 text-xs text-[#F5F5F5] bg-[#161616] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none focus:border-[rgba(214,179,106,0.5)] placeholder-[#52525B]"
            />
          </div>

          {/* Status Filter */}
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-2.5 py-1.5 text-xs text-[#A1A1AA] bg-[#161616] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none"
          >
            <option value="all">All Statuses</option>
            <option value="in_progress">In Progress</option>
            <option value="planning">Planning</option>
            <option value="review">Review</option>
            <option value="completed">Completed</option>
          </select>

          {/* Category Filter */}
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="px-2.5 py-1.5 text-xs text-[#A1A1AA] bg-[#161616] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none"
          >
            <option value="all">All Categories</option>
            {categories.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>

          {/* Sort By */}
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="px-2.5 py-1.5 text-xs text-[#A1A1AA] bg-[#161616] border border-[rgba(255,255,255,0.08)] rounded-lg focus:outline-none"
          >
            <option value="progress">Sort by Progress</option>
            <option value="dueDate">Sort by Due Date</option>
            <option value="name">Sort by Name</option>
          </select>
        </div>

        <div className="flex items-center gap-2">
          {/* View Toggles */}
          <div className="flex items-center p-1 bg-[#161616] border border-[rgba(255,255,255,0.08)] rounded-lg">
            <button
              onClick={() => setViewMode("grid")}
              className={`p-1.5 rounded-md ${
                viewMode === "grid" ? "bg-[#252525] text-[#D6B36A]" : "text-[#71717A]"
              }`}
              title="Grid View"
            >
              <LayoutGrid className="w-3.5 h-3.5" />
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
            onClick={() => setCreateModalOpen(true)}
            className="flex items-center gap-1.5 px-3.5 py-1.5 text-xs font-semibold text-[#0E0E0E] bg-[#D6B36A] hover:bg-[#E0C58A] rounded-lg shadow-sm transition-all"
          >
            <FolderPlus className="w-3.5 h-3.5" />
            <span>New Project</span>
          </button>
        </div>
      </div>

      {/* Grid View */}
      {viewMode === "grid" ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {sorted.map((project) => (
            <div
              key={project.id}
              className="flex flex-col justify-between p-5 rounded-2xl bg-[#111111] hover:bg-[#141414] border border-[rgba(255,255,255,0.07)] hover:border-[rgba(214,179,106,0.3)] transition-all group shadow-sm"
            >
              <div>
                <div className="flex items-center justify-between">
                  <span className="px-2 py-0.5 text-[10px] font-medium rounded-full bg-[#1C1C1E] text-[#D6B36A] border border-[rgba(214,179,106,0.2)]">
                    {project.category}
                  </span>
                  <div className="flex items-center gap-1">
                    <span
                      className={`w-2 h-2 rounded-full ${
                        project.health === "healthy" ? "bg-[#10B981]" : "bg-[#F59E0B]"
                      }`}
                      title={`Health: ${project.health}`}
                    />
                    <button
                      onClick={() => handleDelete(project.id)}
                      className="p-1 rounded text-[#71717A] hover:text-[#EF4444] transition-colors"
                      title="Delete Project"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>

                <h3 className="mt-3 text-sm font-semibold text-[#F5F5F5] group-hover:text-[#D6B36A] transition-colors">
                  {project.name}
                </h3>
                <p className="mt-1 text-xs text-[#A1A1AA] line-clamp-2 leading-relaxed">
                  {project.description}
                </p>
              </div>

              <div className="mt-5 pt-4 border-t border-[rgba(255,255,255,0.05)]">
                {/* Progress */}
                <div className="flex items-center justify-between text-[11px] mb-1.5">
                  <span className="text-[#71717A]">
                    {project.taskCount.completed}/{project.taskCount.total} Tasks Completed
                  </span>
                  <span className="font-mono font-medium text-[#F5F5F5]">{project.progress}%</span>
                </div>
                <div className="w-full bg-[#1F1F1F] rounded-full h-1.5 overflow-hidden mb-3">
                  <div
                    className="bg-gradient-to-r from-[#B08D45] to-[#D6B36A] h-full rounded-full transition-all duration-300"
                    style={{ width: `${project.progress}%` }}
                  />
                </div>

                {/* Footer Meta */}
                <div className="flex items-center justify-between text-xs text-[#71717A]">
                  <div className="flex items-center gap-1.5">
                    <Calendar className="w-3.5 h-3.5" />
                    <span className="text-[11px]">{project.dueDate}</span>
                  </div>

                  {/* Team Avatars */}
                  <div className="flex items-center -space-x-1.5">
                    {project.team.slice(0, 3).map((member) => (
                      <img
                        key={member.id}
                        src={member.avatar}
                        alt={member.name}
                        className="w-5 h-5 rounded-full object-cover border border-[#111111]"
                        title={member.name}
                      />
                    ))}
                    {project.team.length > 3 && (
                      <span className="w-5 h-5 rounded-full bg-[#222222] text-[#A1A1AA] text-[9px] flex items-center justify-center border border-[#111111]">
                        +{project.team.length - 3}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        /* List View */
        <div className="overflow-x-auto rounded-2xl bg-[#111111] border border-[rgba(255,255,255,0.08)]">
          <table className="w-full text-left text-xs text-[#A1A1AA]">
            <thead className="bg-[#141414] text-[11px] text-[#71717A] uppercase border-b border-[rgba(255,255,255,0.06)]">
              <tr>
                <th className="px-5 py-3 font-semibold">Project Name</th>
                <th className="px-4 py-3 font-semibold">Category</th>
                <th className="px-4 py-3 font-semibold">Status</th>
                <th className="px-4 py-3 font-semibold">Progress</th>
                <th className="px-4 py-3 font-semibold">Lead</th>
                <th className="px-4 py-3 font-semibold">Due Date</th>
                <th className="px-4 py-3 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[rgba(255,255,255,0.04)]">
              {sorted.map((project) => (
                <tr key={project.id} className="hover:bg-[#161616] transition-colors">
                  <td className="px-5 py-3 font-semibold text-[#F5F5F5]">{project.name}</td>
                  <td className="px-4 py-3 text-[#A1A1AA]">{project.category}</td>
                  <td className="px-4 py-3">
                    <span
                      className={`px-2 py-0.5 text-[10px] font-semibold rounded-full uppercase ${
                        project.status === "completed"
                          ? "bg-[#064E3B] text-[#34D399]"
                          : project.status === "in_progress"
                          ? "bg-[#252014] text-[#D6B36A]"
                          : "bg-[#1E3A8A] text-[#60A5FA]"
                      }`}
                    >
                      {project.status.replace("_", " ")}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-[#222222] rounded-full h-1.5 overflow-hidden">
                        <div
                          className="bg-[#D6B36A] h-full rounded-full"
                          style={{ width: `${project.progress}%` }}
                        />
                      </div>
                      <span className="font-mono text-[11px] text-[#F5F5F5]">{project.progress}%</span>
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-1.5">
                      <img
                        src={project.owner.avatar}
                        alt={project.owner.name}
                        className="w-5 h-5 rounded-full object-cover"
                      />
                      <span className="text-xs text-[#F5F5F5]">{project.owner.name.split(" ")[0]}</span>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-[11px] text-[#71717A]">{project.dueDate}</td>
                  <td className="px-4 py-3 text-right">
                    <button
                      onClick={() => handleDelete(project.id)}
                      className="p-1 rounded text-[#71717A] hover:text-[#EF4444] transition-colors"
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
      <CreateProjectModal
        isOpen={createModalOpen}
        onClose={() => setCreateModalOpen(false)}
      />

      <ConfirmDeleteModal
        isOpen={deleteModalOpen}
        onClose={() => setDeleteModalOpen(false)}
        onConfirm={() => selectedProjectId && deleteProject(selectedProjectId)}
        title="Delete Project Workspace"
        message="Are you sure you want to delete this project? All associated tasks, audit milestones, and records will be purged from the active view."
      />
    </div>
  );
};
