import { Activity } from "@/types";
import { MOCK_TEAM } from "./mock-team";

export const MOCK_ACTIVITIES: Activity[] = [
  {
    id: "act-1",
    type: "task_completed",
    actor: MOCK_TEAM[3], // Devon
    title: "Completed security audit verification",
    description: "Verified SQLite tamper-evident hash chaining across 5,000 transactions.",
    timestamp: "12 minutes ago",
    projectId: "proj-3",
    projectName: "Enterprise Audit Vault",
  },
  {
    id: "act-2",
    type: "task_status_changed",
    actor: MOCK_TEAM[1], // Marcus
    title: "Moved OAuth2 flow to In Progress",
    description: "Began integration of WebAuthn passkey registration endpoints.",
    timestamp: "1 hour ago",
    projectId: "proj-1",
    projectName: "Aether Engine v2.0",
  },
  {
    id: "act-3",
    type: "project_created",
    actor: MOCK_TEAM[0], // Elena
    title: "Created project Cloud Edge Latency Optimizer",
    description: "Initialized project scope, allocated team members, and defined Q1 budget.",
    timestamp: "3 hours ago",
    projectId: "proj-6",
    projectName: "Cloud Edge Latency Optimizer",
  },
  {
    id: "act-4",
    type: "milestone_reached",
    actor: MOCK_TEAM[2], // Sophia
    title: "Design System 3.0 Milestone Achieved",
    description: "Published 100% tokens and passed WCAG AAA contrast verification.",
    timestamp: "Yesterday at 4:30 PM",
    projectId: "proj-5",
    projectName: "Design System 3.0 Refactor",
  },
  {
    id: "act-5",
    type: "task_created",
    actor: MOCK_TEAM[5], // Kaelen
    title: "Added task for TTFT latency benchmarking",
    description: "Created multi-region inference benchmark requirement.",
    timestamp: "Yesterday at 11:15 AM",
    projectId: "proj-4",
    projectName: "Model Intelligence Gateway",
  },
  {
    id: "act-6",
    type: "member_assigned",
    actor: MOCK_TEAM[0], // Elena
    title: "Assigned Aria to Mobile Companion",
    description: "Assigned offline caching architecture and component implementation.",
    timestamp: "2 days ago",
    projectId: "proj-2",
    projectName: "Pulse Mobile Companion",
  },
];
