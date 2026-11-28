"""OpenClone Frontend Engineering & UI/UX Intelligence Package."""

from src.openclone.frontend.accessibility import (
    AccessibilityAuditor,
    AccessibilityAuditResult,
    WCAGRule,
)
from src.openclone.frontend.browser import (
    BrowserEngine,
    BrowserVerificationEngine,
    BrowserVerificationReport,
    ExecutionEnvironment,
    VisualRegressionResult,
)
from src.openclone.frontend.color import (
    ColorIntelligenceEngine,
    ContrastValidationResult,
    ElementType,
)
from src.openclone.frontend.design_system import (
    DesignToken,
    DesignTokenManager,
    ThemeMode,
    TokenHierarchy,
    TokenStatus,
)
from src.openclone.frontend.performance import (
    CoreWebVitalsBudget,
    PerformanceAuditResult,
    PerformanceBudgetAuditor,
)
from src.openclone.frontend.quality_gate import (
    ComponentState,
    FrontendQualityGate,
    FrontendScorecard,
    GateStatus,
    QualityGateResult,
    evaluate_component_states,
)
from src.openclone.frontend.responsive import (
    ResponsiveAuditResult,
    ResponsiveMatrixAuditor,
    TaskVerificationLevel,
    ViewportCategory,
)
from src.openclone.frontend.security import (
    FrontendSecurityAuditor,
    SecurityAuditResult,
    SecurityFinding,
    SecuritySeverity,
)
from src.openclone.frontend.typography import (
    FontAvailability,
    FontCategory,
    FontEntry,
    FontRegistry,
    TypographyIntelligenceEngine,
)
from src.openclone.frontend.workflow import (
    FrontendLifecycleWorkflow,
    PhaseExecution,
    TaskExecutionLevel,
    WorkflowExecutionResult,
    WorkflowPhase,
)

__all__ = [
    "AccessibilityAuditor",
    "AccessibilityAuditResult",
    "BrowserEngine",
    "BrowserVerificationEngine",
    "BrowserVerificationReport",
    "ColorIntelligenceEngine",
    "ComponentState",
    "ContrastValidationResult",
    "CoreWebVitalsBudget",
    "DesignToken",
    "DesignTokenManager",
    "ElementType",
    "ExecutionEnvironment",
    "FontAvailability",
    "FontCategory",
    "FontEntry",
    "FontRegistry",
    "FrontendLifecycleWorkflow",
    "FrontendQualityGate",
    "FrontendScorecard",
    "FrontendSecurityAuditor",
    "GateStatus",
    "PerformanceAuditResult",
    "PerformanceBudgetAuditor",
    "PhaseExecution",
    "QualityGateResult",
    "ResponsiveAuditResult",
    "ResponsiveMatrixAuditor",
    "SecurityAuditResult",
    "SecurityFinding",
    "SecuritySeverity",
    "TaskExecutionLevel",
    "TaskVerificationLevel",
    "ThemeMode",
    "TokenHierarchy",
    "TokenStatus",
    "TypographyIntelligenceEngine",
    "ViewportCategory",
    "VisualRegressionResult",
    "WorkflowExecutionResult",
    "WorkflowPhase",
    "evaluate_component_states",
]
