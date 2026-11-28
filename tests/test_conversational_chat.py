"""Automated tests for OpenClone Headless Conversational Chat Engine."""
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.openclone.chat.assistant import ConversationalAssistant
from src.openclone.chat.context import ProjectContextCollector
from src.openclone.chat.models import (
    ChatMessage,
    ConversationSession,
    IntentType,
    MessageRole,
)
from src.openclone.mie.contracts import BaseProvider, CompletionResponse


@pytest.fixture
def repo_root():
    return REPO_ROOT


class TestProjectContextCollector:
    """Validate project context gathering and system prompt generation."""

    def test_gather_context(self, repo_root):
        collector = ProjectContextCollector(repo_root)
        ctx = collector.gather_context()
        assert ctx["workspace_name"] == repo_root.name
        assert "Python" in ctx["tech_stack"]
        assert ctx["git"]["is_git"] is True

    def test_format_system_prompt(self, repo_root):
        collector = ProjectContextCollector(repo_root)
        prompt = collector.format_system_prompt()
        assert "OpenClone" in prompt
        assert "Universal AI Engineering Platform" in prompt


class TestConversationSession:
    """Validate multi-turn session history."""

    def test_session_history_and_clear(self, repo_root):
        session = ConversationSession(workspace_root=repo_root)
        assert len(session.messages) == 0

        msg1 = session.add_message(MessageRole.USER, "How do I build a microservice?")
        msg2 = session.add_message(MessageRole.ASSISTANT, "Use OpenClone workflow WF-001.")
        assert len(session.messages) == 2
        assert msg1.role == MessageRole.USER
        assert msg2.role == MessageRole.ASSISTANT

        recent = session.get_recent_history(limit=1)
        assert len(recent) == 1
        assert recent[0].content == "Use OpenClone workflow WF-001."

        session.clear()
        assert len(session.messages) == 0


class TestConversationalAssistant:
    """Validate headless assistant response generation."""

    def test_handle_chat_inspect_flow(self, repo_root):
        assistant = ConversationalAssistant(repo_root)
        with patch.object(assistant, "get_configured_provider", return_value=None):
            res = assistant.handle_chat("Inspect the repository")
            assert res["status"] == "success"
            assert "OpenClone Workspace Inspection" in res["reply"]
            assert res["provider"] == "deterministic_local"

    def test_handle_chat_plan_flow(self, repo_root):
        assistant = ConversationalAssistant(repo_root)
        with patch.object(assistant, "get_configured_provider", return_value=None):
            res = assistant.handle_chat("Plan rate limiter middleware")
            assert res["status"] == "success"
            assert "OpenClone Engineering Task Plan" in res["reply"]
            assert "rate limiter middleware" in res["reply"]

    def test_truthful_missing_provider_message(self, repo_root):
        assistant = ConversationalAssistant(repo_root)
        with patch.object(assistant, "get_configured_provider", return_value=None):
            res = assistant.handle_chat("How do I optimize SQL queries?")
            assert res["status"] == "success"
            assert "No external AI model provider is currently configured" in res["reply"]
            assert "GEMINI_API_KEY" in res["reply"]

    def test_real_provider_inference_flow(self, repo_root):
        assistant = ConversationalAssistant(repo_root)
        mock_provider = MagicMock(spec=BaseProvider)
        mock_provider.display_name = "Mock Gemini Provider"
        mock_provider.complete.return_value = CompletionResponse(
            content="Here is how to optimize your SQL query in OpenClone...",
            model="gemini-2.0-flash",
            provider_id="gemini",
        )

        with patch.object(assistant, "get_configured_provider", return_value=("gemini", mock_provider)):
            res = assistant.handle_chat("How do I optimize SQL queries?")
            assert res["status"] == "success"
            assert "optimize your SQL query" in res["reply"]
            assert res["provider"] == "gemini"
