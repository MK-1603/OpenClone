"""Mermaid System Design Diagram Generator.

Produces C4 Context, Container, Component, Sequence, and Data Flow diagrams
in clean, valid, GitHub-renderable Mermaid markdown.
"""
from __future__ import annotations

from typing import List, Optional


class SystemDiagramGenerator:
    """Generates deterministic Mermaid diagrams for system design documentation."""

    @staticmethod
    def generate_c4_context(
        system_name: str,
        user_types: List[str],
        external_systems: List[str],
        core_description: str,
    ) -> str:
        """Render a C4 Context Diagram in Mermaid syntax."""
        lines = [
            "```mermaid",
            "flowchart TD",
            "    %% C4 Context Diagram",
        ]
        for idx, u in enumerate(user_types):
            u_id = f"user_{idx}"
            lines.append(f'    {u_id}["👤 {u}"]')

        lines.append(f'    core_sys[["💻 {system_name}<br/>({core_description})"]]')

        for idx, ext in enumerate(external_systems):
            ext_id = f"ext_{idx}"
            lines.append(f'    {ext_id}["🏢 {ext}"]')

        for idx in range(len(user_types)):
            lines.append(f'    user_{idx} -->|"Interacts via Web/Mobile"| core_sys')

        for idx in range(len(external_systems)):
            lines.append(f'    core_sys -->|"Integrates with"| ext_{idx}')

        lines.append("```")
        return "\n".join(lines)

    @staticmethod
    def generate_c4_container(
        system_name: str,
        containers: List[dict],
    ) -> str:
        """Render a C4 Container Diagram showing web app, API, DB, cache, and queues."""
        lines = [
            "```mermaid",
            "flowchart LR",
            f"    subgraph {system_name} [System Boundary: {system_name}]",
        ]
        for c in containers:
            c_id = c["id"]
            c_name = c["name"]
            c_tech = c["technology"]
            c_desc = c.get("description", "")
            lines.append(f'        {c_id}["📦 {c_name}<br/><b>[{c_tech}]</b><br/>{c_desc}"]')

        lines.append("    end")
        lines.append("```")
        return "\n".join(lines)

    @staticmethod
    def generate_sequence_diagram(
        title: str,
        participants: List[str],
        steps: List[tuple],  # (from, to, action_text)
    ) -> str:
        """Render a sequence diagram showing request flow across components."""
        lines = [
            "```mermaid",
            "sequenceDiagram",
            f"    autonumber",
        ]
        for p in participants:
            lines.append(f"    participant {p}")

        for sender, receiver, text in steps:
            lines.append(f"    {sender}->>{receiver}: {text}")

        lines.append("```")
        return "\n".join(lines)

    @staticmethod
    def generate_data_flow(
        flow_name: str,
        stages: List[str],
    ) -> str:
        """Render an end-to-end data flow pipeline diagram."""
        lines = [
            "```mermaid",
            "flowchart LR",
            f"    %% Data Flow: {flow_name}",
        ]
        for i, s in enumerate(stages):
            node_id = f"stage_{i}"
            lines.append(f'    {node_id}["{s}"]')
            if i > 0:
                prev_id = f"stage_{i-1}"
                lines.append(f"    {prev_id} --> {node_id}")

        lines.append("```")
        return "\n".join(lines)
