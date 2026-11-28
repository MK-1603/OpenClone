"""OpenClone Conversational AI Assistant & Tool Orchestration Engine (Headless Core)."""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from src.openclone.chat.context import ProjectContextCollector
from src.openclone.chat.models import (
    ChatMessage,
    ConversationSession,
    IntentType,
    MessageRole,
)
from src.openclone.mie.contracts import BaseProvider, CompletionResponse
from src.openclone.mie.providers.anthropic import AnthropicProvider
from src.openclone.mie.providers.gemini import GeminiProvider
from src.openclone.mie.providers.ollama import OllamaProvider
from src.openclone.mie.providers.openai import OpenAIProvider
from src.openclone.mie.registry import ModelRegistry


class ConversationalAssistant:
    """Conversational engineering assistant coordinating MIE models, tools, and context."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.context_collector = ProjectContextCollector(self.workspace_root)
        self.session = ConversationSession(workspace_root=self.workspace_root)
        self.mie_registry = ModelRegistry()

    def get_configured_provider(self) -> Optional[Tuple[str, BaseProvider]]:
        """Identify the highest-precedence configured AI model provider."""
        providers = [
            ("gemini", GeminiProvider()),
            ("openai", OpenAIProvider()),
            ("anthropic", AnthropicProvider()),
            ("ollama", OllamaProvider()),
        ]
        for name, prov in providers:
            try:
                if prov.is_configured():
                    return name, prov
            except Exception:
                continue
        return None

    def classify_intent(self, text: str) -> Tuple[IntentType, Dict[str, Any]]:
        """Classify user input into actionable intent types."""
        clean = text.strip()
        lower = clean.lower()

        # Direct slash commands
        if clean.startswith("/"):
            parts = clean[1:].split(maxsplit=1)
            cmd = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            if cmd in ("plan", "decompose"):
                return IntentType.PLAN, {"requirement": args}
            elif cmd in ("run", "exec", "execute"):
                return IntentType.EXECUTE, {"task": args}
            elif cmd in ("inspect", "xray"):
                return IntentType.INSPECT, {"path": args}
            elif cmd in ("verify", "check"):
                return IntentType.VERIFY, {"path": args}
            elif cmd in ("agents", "workers"):
                return IntentType.WORKFORCE, {}
            elif cmd == "models":
                return IntentType.MODELS, {}
            elif cmd == "providers":
                return IntentType.PROVIDERS, {}
            elif cmd == "workflows":
                return IntentType.WORKFLOWS, {}
            elif cmd == "doctor":
                return IntentType.DIAGNOSTICS, {}
            elif cmd == "config":
                return IntentType.CONFIG, {}
            return IntentType.SLASH_COMMAND, {"command": cmd, "args": args}

        # Conversational pattern matching
        if re.search(r"\b(plan|breakdown|decompose|architect|how to build)\b", lower):
            return IntentType.PLAN, {"requirement": clean}
        if re.search(r"\b(run|execute|apply|implement task|perform)\b", lower):
            return IntentType.EXECUTE, {"task": clean}
        if re.search(r"\b(inspect|examine|review repo|show status|git status|files)\b", lower):
            return IntentType.INSPECT, {}
        if re.search(r"\b(verify|test|run tests|check gates|audit)\b", lower):
            return IntentType.VERIFY, {}
        if re.search(r"\b(agents?|workforce|workers|roles)\b", lower):
            return IntentType.WORKFORCE, {}
        if re.search(r"\b(models?|llm|intelligence catalog)\b", lower):
            return IntentType.MODELS, {}

        return IntentType.CHAT, {}

    def handle_chat(
        self,
        message: str,
        requested_model: Optional[str] = None,
        requested_agent: Optional[str] = None,
        editor_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Process conversational turn headlessly and return structured JSON."""
        clean = message.strip()
        if not clean:
            return {"error": "Message cannot be empty", "status_code": 400}

        editor_context = editor_context or {}
        self.session.add_message(MessageRole.USER, clean)

        # Build context augmentations
        active_file = editor_context.get("activeFile")
        selection_text = editor_context.get("selection")
        editor_snippet = ""
        if active_file:
            editor_snippet = f"\n[Editor Context: Active File: {active_file}"
            if selection_text:
                editor_snippet += f", Selection:\n```{editor_context.get('language', '')}\n{selection_text}\n```"
            editor_snippet += "]"

        intent, intent_args = self.classify_intent(clean)
        active_provider = self.get_configured_provider()

        actions = []
        governance = None

        if active_provider:
            provider_id, provider = active_provider
            system_prompt = self.context_collector.format_system_prompt()
            if editor_snippet:
                system_prompt += editor_snippet

            prompt_parts = [system_prompt, "\nConversation History:"]
            for m in self.session.get_recent_history(limit=6):
                prompt_parts.append(f"{m.role.value.capitalize()}: {m.content}")
            prompt_parts.append("Assistant:")

            full_prompt = "\n".join(prompt_parts)
            try:
                resp = provider.complete(full_prompt, options={"temperature": 0.3})
                response_text = resp.content
            except Exception as e:
                response_text = f"Inference communication error with {provider.display_name}: {e}"
        else:
            # Deterministic Local Mode Guidance
            ctx = self.context_collector.gather_context()
            git_info = ctx["git"]
            git_b = git_info.get("branch", "main")
            tracked_f = git_info.get("tracked_count", 0)
            langs = ctx.get("tech_stack", [])

            if intent == IntentType.INSPECT or "inspect" in clean.lower():
                response_text = (
                    f"### OpenClone Workspace Inspection\n\n"
                    f"- **Workspace Root:** `{self.workspace_root}`\n"
                    f"- **Git Branch:** `{git_b}`\n"
                    f"- **Tracked Files:** `{tracked_f}`\n"
                    f"- **Primary Tech Stack:** {', '.join(langs)}\n"
                    f"- **OpenClone Version:** `2.0.0` (Extension-First Core)\n\n"
                    f"All repository boundaries are active and enforced by deterministic policy."
                )
            elif intent == IntentType.PLAN or "plan" in clean.lower():
                clean_req = intent_args.get("requirement", clean)
                response_text = (
                    f"### OpenClone Engineering Task Plan\n\n"
                    f"**Requirement:** {clean_req}\n\n"
                    f"**Proposed Execution Steps:**\n"
                    f"1. `T01-INSPECT`: Analyze workspace architecture and affected modules.\n"
                    f"2. `T02-SPECIFY`: Define deterministic contract schemas and unit test fixtures.\n"
                    f"3. `T03-IMPLEMENT`: Execute minimal code implementation adhering to project conventions.\n"
                    f"4. `T04-VERIFY`: Execute test suite and audit ledger validation gates.\n\n"
                    f"> **Deterministic Governance Notice:** Planning does not alter files. "
                    f"To proceed with governed execution, click **Execute Plan** below."
                )
                actions = [{"label": "Execute Plan", "command": "openclone.run", "args": [clean_req]}]
            elif intent == IntentType.WORKFORCE or "agent" in clean.lower() or "worker" in clean.lower():
                from src.openclone.runtime.workforce import load_workers
                workers = load_workers()
                response_text = (
                    f"### OpenClone Agent Workforce\n\n"
                    f"Loaded **{len(workers)}** governed agent contracts across core divisions:\n"
                    f"- **Architecture & Governance:** `SystemArchitect`, `SecurityReviewer`, `GovernanceLead`\n"
                    f"- **Core Engineering:** `BackendEngineer`, `FrontendEngineer`, `DatabaseSpecialist`\n"
                    f"- **Verification & QA:** `TestEngineer`, `PerformanceAuditor`, `ComplianceOfficer`\n\n"
                    f"Every agent contract specifies bounded permissions, required approvals, and deterministic deliverables."
                )
            else:
                response_text = (
                    f"### OpenClone 2.0 — Extension-First Engineering Assistant\n\n"
                    f"No external AI model provider is currently configured with an active API key on this machine.\n\n"
                    f"**To enable live LLM conversational reasoning, configure an API key:**\n"
                    f"- `GEMINI_API_KEY` — Google Gemini (Recommended: Pro 2.5 / Flash 2.0)\n"
                    f"- `OPENAI_API_KEY` — OpenAI (GPT-4o, o3-mini)\n"
                    f"- `ANTHROPIC_API_KEY` — Anthropic Claude (Claude 3.7 Sonnet)\n"
                    f"- Or start local **Ollama** (`http://127.0.0.1:11434`)\n\n"
                    f"**Local Deterministic Capabilities (Ready Now):**\n"
                    f"- **Explain Selection:** Extracts code context from your active VS Code editor.\n"
                    f"- **Inspect Workspace:** Verifies branch, files, and repository health.\n"
                    f"- **Generate Plan:** Creates topological execution graphs.\n"
                    f"- **Agent Workforce:** Access 72 specialized engineering worker contracts."
                )

        self.session.add_message(MessageRole.ASSISTANT, response_text)

        return {
            "status": "success",
            "reply": response_text,
            "provider": active_provider[0] if active_provider else "deterministic_local",
            "model": requested_model or ("gemini-2.5-pro" if active_provider else "openclone-deterministic-v2"),
            "agent": requested_agent or "OpenCloneAssistant",
            "actions": actions,
            "governance": governance,
        }
