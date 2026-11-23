export type ProjectStatus = "planning" | "in_progress" | "review" | "completed" | "on_hold";
export type ProjectPriority = "low" | "medium" | "high" | "critical";
export type ProjectHealth = "healthy" | "at_risk" | "critical";

export type TaskStatus = "backlog" | "todo" | "in_progress" | "review" | "completed";
export type TaskPriority = "low" | "medium" | "high" | "urgent";

export interface TeamMember {
  id: string;
  name: string;
  email: string;
  role: string;
  department: string;
  avatar: string;
  activeTasks: number;
  completedTasks: number;
  workloadPercent: number;
  status: "active" | "in_meeting" | "offline";
}

export interface Project {
  id: string;
  name: string;
  description: string;
  status: ProjectStatus;
  priority: ProjectPriority;
  category: string;
  progress: number;
  owner: TeamMember;
  team: TeamMember[];
  startDate: string;
  dueDate: string;
  budget: string;
  health: ProjectHealth;
  taskCount: {
    total: number;
    completed: number;
  };
}

export interface Task {
  id: string;
  title: string;
  description: string;
  status: TaskStatus;
  priority: TaskPriority;
  projectId: string;
  projectName: string;
  assignee: TeamMember;
  dueDate: string;
  estimatedHours: number;
  tags: string[];
}

export interface Activity {
  id: string;
  type: "task_created" | "task_completed" | "task_status_changed" | "project_created" | "member_assigned" | "milestone_reached";
  actor: TeamMember;
  title: string;
  description: string;
  timestamp: string;
  projectId?: string;
  projectName?: string;
}

export interface CalendarEvent {
  id: string;
  title: string;
  date: string;
  type: "deadline" | "milestone" | "review" | "meeting";
  projectId: string;
  projectName: string;
  priority: ProjectPriority;
}

export interface WorkspaceSettings {
  workspaceName: string;
  theme: "dark" | "charcoal" | "oled";
  accentColor: string;
  emailNotifications: boolean;
  desktopNotifications: boolean;
  compactView: boolean;
  autoSaveInterval: number;
}
