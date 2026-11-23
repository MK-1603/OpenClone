"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { Project, Task, TeamMember, Activity, WorkspaceSettings, TaskStatus } from "@/types";
import { MOCK_PROJECTS } from "@/data/mock-projects";
import { MOCK_TASKS } from "@/data/mock-tasks";
import { MOCK_TEAM } from "@/data/mock-team";
import { MOCK_ACTIVITIES } from "@/data/mock-activities";

interface PulseContextType {
  projects: Project[];
  tasks: Task[];
  team: TeamMember[];
  activities: Activity[];
  settings: WorkspaceSettings;
  searchQuery: string;
  setSearchQuery: (q: string) => void;
  addProject: (p: Omit<Project, "id" | "progress" | "taskCount">) => void;
  updateProject: (id: string, updates: Partial<Project>) => void;
  deleteProject: (id: string) => void;
  addTask: (t: Omit<Task, "id">) => void;
  updateTask: (id: string, updates: Partial<Task>) => void;
  deleteTask: (id: string) => void;
  updateTaskStatus: (taskId: string, newStatus: TaskStatus) => void;
  updateSettings: (s: Partial<WorkspaceSettings>) => void;
  quickCreateOpen: boolean;
  setQuickCreateOpen: (open: boolean) => void;
}

const DEFAULT_SETTINGS: WorkspaceSettings = {
  workspaceName: "Aether Labs Global",
  theme: "charcoal",
  accentColor: "#D6B36A",
  emailNotifications: true,
  desktopNotifications: true,
  compactView: false,
  autoSaveInterval: 30,
};

const PulseContext = createContext<PulseContextType | undefined>(undefined);

export const PulseProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [projects, setProjects] = useState<Project[]>(MOCK_PROJECTS);
  const [tasks, setTasks] = useState<Task[]>(MOCK_TASKS);
  const [team] = useState<TeamMember[]>(MOCK_TEAM);
  const [activities, setActivities] = useState<Activity[]>(MOCK_ACTIVITIES);
  const [settings, setSettings] = useState<WorkspaceSettings>(DEFAULT_SETTINGS);
  const [searchQuery, setSearchQuery] = useState("");
  const [quickCreateOpen, setQuickCreateOpen] = useState(false);

  // Load from localStorage on mount (client-side only)
  useEffect(() => {
    try {
      const savedProjects = localStorage.getItem("pulse_projects");
      if (savedProjects) setProjects(JSON.parse(savedProjects));

      const savedTasks = localStorage.getItem("pulse_tasks");
      if (savedTasks) setTasks(JSON.parse(savedTasks));

      const savedSettings = localStorage.getItem("pulse_settings");
      if (savedSettings) setSettings(JSON.parse(savedSettings));
    } catch {
      // Ignore fallback
    }
  }, []);

  // Save changes to localStorage
  const saveProjects = (newProjects: Project[]) => {
    setProjects(newProjects);
    try {
      localStorage.setItem("pulse_projects", JSON.stringify(newProjects));
    } catch {}
  };

  const saveTasks = (newTasks: Task[]) => {
    setTasks(newTasks);
    try {
      localStorage.setItem("pulse_tasks", JSON.stringify(newTasks));
    } catch {}
  };

  const addProject = (p: Omit<Project, "id" | "progress" | "taskCount">) => {
    const newProj: Project = {
      ...p,
      id: `proj-${Date.now()}`,
      progress: 0,
      taskCount: { total: 0, completed: 0 },
    };
    const updated = [newProj, ...projects];
    saveProjects(updated);

    const act: Activity = {
      id: `act-${Date.now()}`,
      type: "project_created",
      actor: team[0],
      title: `Created project ${newProj.name}`,
      description: newProj.description,
      timestamp: "Just now",
      projectId: newProj.id,
      projectName: newProj.name,
    };
    setActivities([act, ...activities]);
  };

  const updateProject = (id: string, updates: Partial<Project>) => {
    const updated = projects.map((p) => (p.id === id ? { ...p, ...updates } : p));
    saveProjects(updated);
  };

  const deleteProject = (id: string) => {
    const updated = projects.filter((p) => p.id !== id);
    saveProjects(updated);
    // Also remove associated tasks
    const remainingTasks = tasks.filter((t) => t.projectId !== id);
    saveTasks(remainingTasks);
  };

  const addTask = (t: Omit<Task, "id">) => {
    const newTask: Task = {
      ...t,
      id: `task-${Date.now()}`,
    };
    const updated = [newTask, ...tasks];
    saveTasks(updated);

    // Update project task count
    if (t.projectId) {
      setProjects((prev) =>
        prev.map((proj) =>
          proj.id === t.projectId
            ? {
                ...proj,
                taskCount: {
                  ...proj.taskCount,
                  total: proj.taskCount.total + 1,
                  completed: t.status === "completed" ? proj.taskCount.completed + 1 : proj.taskCount.completed,
                },
              }
            : proj
        )
      );
    }

    const act: Activity = {
      id: `act-${Date.now()}`,
      type: "task_created",
      actor: team[0],
      title: `Added task "${newTask.title}"`,
      description: `Assigned to ${newTask.assignee.name} under ${newTask.projectName}`,
      timestamp: "Just now",
      projectId: newTask.projectId,
      projectName: newTask.projectName,
    };
    setActivities([act, ...activities]);
  };

  const updateTask = (id: string, updates: Partial<Task>) => {
    const updated = tasks.map((t) => (t.id === id ? { ...t, ...updates } : t));
    saveTasks(updated);
  };

  const updateTaskStatus = (taskId: string, newStatus: TaskStatus) => {
    const task = tasks.find((t) => t.id === taskId);
    if (!task || task.status === newStatus) return;

    const oldStatus = task.status;
    const updated = tasks.map((t) => (t.id === taskId ? { ...t, status: newStatus } : t));
    saveTasks(updated);

    // Update project stats if completed
    if (newStatus === "completed" && oldStatus !== "completed") {
      setProjects((prev) =>
        prev.map((p) =>
          p.id === task.projectId
            ? { ...p, taskCount: { ...p.taskCount, completed: p.taskCount.completed + 1 } }
            : p
        )
      );
    } else if (oldStatus === "completed" && newStatus !== "completed") {
      setProjects((prev) =>
        prev.map((p) =>
          p.id === task.projectId
            ? { ...p, taskCount: { ...p.taskCount, completed: Math.max(0, p.taskCount.completed - 1) } }
            : p
        )
      );
    }

    const act: Activity = {
      id: `act-${Date.now()}`,
      type: newStatus === "completed" ? "task_completed" : "task_status_changed",
      actor: task.assignee,
      title: `Task ${task.title} updated to ${newStatus.replace("_", " ").toUpperCase()}`,
      description: `Status changed in ${task.projectName}`,
      timestamp: "Just now",
      projectId: task.projectId,
      projectName: task.projectName,
    };
    setActivities([act, ...activities]);
  };

  const deleteTask = (id: string) => {
    const task = tasks.find((t) => t.id === id);
    const updated = tasks.filter((t) => t.id !== id);
    saveTasks(updated);

    if (task) {
      setProjects((prev) =>
        prev.map((p) =>
          p.id === task.projectId
            ? {
                ...p,
                taskCount: {
                  total: Math.max(0, p.taskCount.total - 1),
                  completed: task.status === "completed" ? Math.max(0, p.taskCount.completed - 1) : p.taskCount.completed,
                },
              }
            : p
        )
      );
    }
  };

  const updateSettings = (s: Partial<WorkspaceSettings>) => {
    const updated = { ...settings, ...s };
    setSettings(updated);
    try {
      localStorage.setItem("pulse_settings", JSON.stringify(updated));
    } catch {}
  };

  return (
    <PulseContext.Provider
      value={{
        projects,
        tasks,
        team,
        activities,
        settings,
        searchQuery,
        setSearchQuery,
        addProject,
        updateProject,
        deleteProject,
        addTask,
        updateTask,
        deleteTask,
        updateTaskStatus,
        updateSettings,
        quickCreateOpen,
        setQuickCreateOpen,
      }}
    >
      {children}
    </PulseContext.Provider>
  );
};

export const usePulse = () => {
  const context = useContext(PulseContext);
  if (!context) {
    throw new Error("usePulse must be used within a PulseProvider");
  }
  return context;
};
