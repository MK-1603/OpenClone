"""Tests for DocumentIngestionEngine and parsers (Stage 2)."""

from __future__ import annotations

import csv
import io
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.openclone.intelligence.ingestion.engine import DocumentIngestionEngine
from src.openclone.intelligence.ingestion.models import (
    DocumentFormat,
    EvidenceClassification,
    ExtractionStatus,
)
from src.openclone.intelligence.ingestion.parsers import (
    CsvParser,
    DocxParser,
    ImageNoticeParser,
    MarkdownParser,
    PdfParser,
    PlainTextParser,
    XlsxParser,
)
from src.openclone.intelligence.project_intelligence import ProjectIntelligenceArchitect
from src.openclone.system_design.capacity import ComprehensiveCapacityReport


@pytest.fixture
def temp_docs_dir(tmp_path: Path) -> Path:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    return docs_dir


def test_plain_text_parser(temp_docs_dir: Path):
    txt_file = temp_docs_dir / "spec.txt"
    txt_file.write_text("System requirements:\n- Response time < 200ms\n- Scale to 5000 DAU\nConstraint: SQLite only", encoding="utf-8")

    parser = PlainTextParser()
    assert parser.supports_format(DocumentFormat.TXT) is True
    assert parser.supports_format(DocumentFormat.PDF) is False

    doc = parser.parse(txt_file)
    assert doc.status == ExtractionStatus.SUCCESS
    assert "Response time < 200ms" in doc.extracted_text
    assert len(doc.evidence) > 0
    categories = [e.evidence_classification for e in doc.evidence]
    assert EvidenceClassification.REQUIREMENT in categories or EvidenceClassification.TECHNICAL_LIMITATION in categories or EvidenceClassification.WORKLOAD_METRIC in categories


def test_markdown_parser(temp_docs_dir: Path):
    md_file = temp_docs_dir / "architecture.md"
    md_content = """# Architecture Overview
## Requirements
- Requirement: Must support JWT auth
## Workload
DAU: 25000 users
## Constraints
- Constraint: No cloud vendor lock-in
```python
def example():
    pass
```
"""
    md_file.write_text(md_content, encoding="utf-8")

    parser = MarkdownParser()
    doc = parser.parse(md_file)
    assert doc.status == ExtractionStatus.SUCCESS
    assert len(doc.metadata["headings"]) >= 3
    assert any(e.evidence_classification in (EvidenceClassification.REQUIREMENT, EvidenceClassification.WORKLOAD_METRIC) for e in doc.evidence)


def test_csv_parser(temp_docs_dir: Path):
    csv_file = temp_docs_dir / "features.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Type", "Notes"])
        writer.writerow(["F01", "User Login", "Requirement", "OAuth2 support must be used"])
        writer.writerow(["F02", "Peak Load", "Metric", "1000 RPS peak load"])

    parser = CsvParser()
    doc = parser.parse(csv_file)
    assert doc.status == ExtractionStatus.SUCCESS
    assert doc.metadata["row_count"] >= 2
    assert "User Login" in doc.extracted_text
    assert any(e.evidence_classification in (EvidenceClassification.REQUIREMENT, EvidenceClassification.WORKLOAD_METRIC, EvidenceClassification.DATA_SCHEMA) for e in doc.evidence)


def test_docx_parser_real_file(temp_docs_dir: Path):
    import docx

    doc_path = temp_docs_dir / "document.docx"
    d = docx.Document()
    d.add_heading("Product Requirements", level=1)
    d.add_paragraph("Requirement: System must handle real-time notifications.")
    d.add_paragraph("Constraint: Must run on Ubuntu 24.04 LTS.")
    table = d.add_table(rows=2, cols=2)
    table.cell(0, 0).text = "Metric"
    table.cell(0, 1).text = "Target"
    table.cell(1, 0).text = "Workload"
    table.cell(1, 1).text = "100000 DAU"
    d.save(str(doc_path))

    parser = DocxParser()
    doc = parser.parse(doc_path)
    assert doc.status == ExtractionStatus.SUCCESS
    assert "Product Requirements" in doc.extracted_text
    assert "notifications" in doc.extracted_text
    assert "100000 DAU" in doc.extracted_text
    assert any(e.evidence_classification in (EvidenceClassification.WORKLOAD_METRIC, EvidenceClassification.REQUIREMENT) for e in doc.evidence)


def test_pdf_parser_missing_dependency_graceful(temp_docs_dir: Path):
    pdf_file = temp_docs_dir / "spec.pdf"
    pdf_file.write_bytes(b"%PDF-1.4 dummy content")

    parser = PdfParser()
    with patch.dict("sys.modules", {"pypdf": None}):
        doc = parser.parse(pdf_file)
        assert doc.status == ExtractionStatus.MISSING_DEPENDENCY
        assert "pypdf" in (doc.error_message or "")


def test_pdf_parser_mocked_success(temp_docs_dir: Path):
    pdf_file = temp_docs_dir / "spec.pdf"
    pdf_file.write_bytes(b"%PDF-1.4 dummy")

    mock_page = MagicMock()
    mock_page.extract_text.return_value = "Requirement: High-throughput ingestion\nPeak load: 5000 RPS"
    mock_reader = MagicMock()
    mock_reader.pages = [mock_page]

    with patch.dict("sys.modules", {"pypdf": MagicMock(PdfReader=MagicMock(return_value=mock_reader))}):
        parser = PdfParser()
        doc = parser.parse(pdf_file)
        assert doc.status == ExtractionStatus.SUCCESS
        assert "High-throughput" in doc.extracted_text
        assert any(e.evidence_classification in (EvidenceClassification.WORKLOAD_METRIC, EvidenceClassification.REQUIREMENT) for e in doc.evidence)


def test_xlsx_parser_missing_dependency_graceful(temp_docs_dir: Path):
    xlsx_file = temp_docs_dir / "metrics.xlsx"
    xlsx_file.write_bytes(b"PK dummy zip")

    parser = XlsxParser()
    with patch.dict("sys.modules", {"openpyxl": None}):
        doc = parser.parse(xlsx_file)
        assert doc.status == ExtractionStatus.MISSING_DEPENDENCY
        assert "openpyxl" in (doc.error_message or "")


def test_image_notice_parser(temp_docs_dir: Path):
    img_file = temp_docs_dir / "diagram.png"
    img_file.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR")

    parser = ImageNoticeParser()
    doc = parser.parse(img_file)
    assert doc.status == ExtractionStatus.PARTIAL
    assert doc.metadata["requires_vision_model"] is True
    assert len(doc.warnings) > 0


def test_engine_format_detection_and_file_size_limit(temp_docs_dir: Path):
    engine = DocumentIngestionEngine(max_file_size_bytes=100)
    big_file = temp_docs_dir / "big.txt"
    big_file.write_text("A" * 200, encoding="utf-8")

    doc = engine.ingest_file(big_file)
    assert doc.status == ExtractionStatus.EXCEEDS_SIZE_LIMIT
    assert "exceeds" in (doc.error_message or "").lower()


def test_engine_directory_scanning_and_evidence(temp_docs_dir: Path):
    f1 = temp_docs_dir / "doc1.txt"
    f1.write_text("Requirement: Feature Alpha must be supported.\nWorkload: 10000 DAU", encoding="utf-8")
    f2 = temp_docs_dir / "doc2.md"
    f2.write_text("# Title\nConstraint: SQLite single-writer constraint", encoding="utf-8")

    engine = DocumentIngestionEngine()
    docs = engine.ingest_directory(temp_docs_dir)
    assert len(docs) >= 2

    evidence = engine.extract_evidence(docs)
    assert len(evidence) >= 2
    sources = {e.file_name for e in evidence}
    assert "doc1.txt" in sources
    assert "doc2.md" in sources


def test_pia_integration_with_documents(temp_docs_dir: Path):
    doc_path = temp_docs_dir / "requirements.txt"
    doc_path.write_text("Feature FEAT-CORE: High-speed sync\nWorkload: 50000 daily active users\nConstraint: Zero data loss", encoding="utf-8")

    pia = ProjectIntelligenceArchitect()
    result = pia.execute_new(
        prompt="Design an enterprise sync system",
        project_name="SyncEngine",
        document_paths=[doc_path],
    )

    assert "ingested_documents" in result
    assert len(result["ingested_documents"]) == 1
    assert result["ingested_documents"][0]["file_name"] == "requirements.txt"
    # Verify workload in Set C was picked up from ingested doc without synthetic assumption
    set_c = result["set_c_solutions"]
    cap_rep = set_c["capacity_report"]
    assert isinstance(cap_rep, ComprehensiveCapacityReport)
    assert cap_rep.traffic.daily_active_users == 50000


def test_pia_defined_with_documents(temp_docs_dir: Path):
    doc_path = temp_docs_dir / "extra_notes.md"
    doc_path.write_text("## Extra Information\nRequirement: Audit logging must be enabled", encoding="utf-8")

    pia = ProjectIntelligenceArchitect()
    docs = {"main.md": "# Main\nBasic API description"}
    result = pia.execute_defined(
        documents=docs,
        project_name="DefinedSystem",
        document_paths=[doc_path],
    )

    assert "ingested_documents" in result
    assert len(result["ingested_documents"]) == 1
    assert result["ingested_documents"][0]["file_name"] == "extra_notes.md"
