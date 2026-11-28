"""Data models and classifications for Document Ingestion Subsystem."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class DocumentFormat(str, Enum):
    """Supported document formats."""
    TXT = "txt"
    MARKDOWN = "markdown"
    CSV = "csv"
    PDF = "pdf"
    DOCX = "docx"
    XLSX = "xlsx"
    IMAGE = "image"
    UNKNOWN = "unknown"


class ExtractionStatus(str, Enum):
    """Status of document extraction."""
    SUCCESS = "success"
    PARTIAL = "partial"
    UNSUPPORTED = "unsupported"
    MISSING_DEPENDENCY = "missing_dependency"
    SCANNED_PDF_NO_TEXT = "scanned_pdf_no_text"
    CORRUPTED = "corrupted"
    EXCEEDS_SIZE_LIMIT = "exceeds_size_limit"
    ERROR = "error"


class EvidenceClassification(str, Enum):
    """Taxonomy of extracted project intelligence evidence."""
    REQUIREMENT = "requirement"
    TECHNICAL_LIMITATION = "technical_limitation"
    ARCHITECTURE_HINT = "architecture_hint"
    UNCONFIRMED_RECOMMENDATION = "unconfirmed_recommendation"
    WORKLOAD_METRIC = "workload_metric"
    DATA_SCHEMA = "data_schema"
    GENERAL_CONTEXT = "general_context"


@dataclass
class ExtractedEvidence:
    """Discrete evidence item extracted from an ingested document with source attribution."""
    evidence_id: str
    source_document: str
    file_name: str
    document_type: str
    section_or_location: str
    content: str
    evidence_classification: EvidenceClassification = EvidenceClassification.GENERAL_CONTEXT
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "source_document": self.source_document,
            "file_name": self.file_name,
            "document_type": self.document_type,
            "section_or_location": self.section_or_location,
            "content": self.content,
            "evidence_classification": self.evidence_classification.value,
            "confidence": round(self.confidence, 3),
            "metadata": self.metadata,
        }


@dataclass
class IngestedDocument:
    """Normalized ingested document with extracted text, structure, metadata, and evidence."""
    file_path: str
    file_name: str
    detected_format: DocumentFormat
    status: ExtractionStatus
    raw_text: str = ""
    structured_data: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    evidence_items: List[ExtractedEvidence] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_path": self.file_path,
            "file_name": self.file_name,
            "detected_format": self.detected_format.value,
            "status": self.status.value,
            "text_length": len(self.raw_text),
            "metadata": self.metadata,
            "evidence_count": len(self.evidence_items),
            "evidence_items": [e.to_dict() for e in self.evidence_items],
            "warnings": self.warnings,
            "error_message": self.error_message,
        }

    @property
    def extracted_text(self) -> str:
        return self.raw_text

    @property
    def evidence(self) -> List[ExtractedEvidence]:
        return self.evidence_items

    @property
    def format(self) -> DocumentFormat:
        return self.detected_format

    @property
    def path(self) -> Path:
        return Path(self.file_path)
