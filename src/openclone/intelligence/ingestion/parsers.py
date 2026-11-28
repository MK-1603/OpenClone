"""Modular parsers for distinct document formats."""
from __future__ import annotations

import abc
import csv
import io
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from src.openclone.intelligence.ingestion.models import (
    DocumentFormat,
    EvidenceClassification,
    ExtractionStatus,
    ExtractedEvidence,
    IngestedDocument,
)


class BaseDocumentParser(abc.ABC):
    """Abstract base class for format-specific document parsers."""

    @abc.abstractmethod
    def can_parse(self, doc_format: DocumentFormat) -> bool:
        """Check if parser can handle given format."""
        raise NotImplementedError

    def supports_format(self, doc_format: DocumentFormat) -> bool:
        """Alias for can_parse."""
        return self.can_parse(doc_format)

    @abc.abstractmethod
    def parse(self, file_path: Path, max_bytes: int = 20 * 1024 * 1024) -> IngestedDocument:
        """Extract text, metadata, and structured data from the document."""
        raise NotImplementedError


def _normalize_text(text: str) -> str:
    """Normalize extracted text by stripping null bytes and carriage returns."""
    if not text:
        return ""
    text = text.replace("\x00", "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.strip()


def _extract_evidence_from_lines(
    lines: List[Tuple[str, str]],
    source_name: str,
    doc_type: str,
) -> List[ExtractedEvidence]:
    """Scan lines for requirements, architectural decisions, and constraints."""
    evidence: List[ExtractedEvidence] = []
    idx = 1
    req_patterns = [
        (re.compile(r"(?i)\b(must|shall|required|mandatory|essential)\b"), EvidenceClassification.REQUIREMENT, 0.95),
        (re.compile(r"(?i)\b(should|recommended|preferred|ought to)\b"), EvidenceClassification.UNCONFIRMED_RECOMMENDATION, 0.75),
        (re.compile(r"(?i)\b(cannot|limitation|constraint|bottleneck|forbidden|restricted)\b"), EvidenceClassification.TECHNICAL_LIMITATION, 0.90),
        (re.compile(r"(?i)\b(database|postgres|mysql|sqlite|mongodb|redis|kafka|architecture|c4|microservice|monolith|rest api|graphql)\b"), EvidenceClassification.ARCHITECTURE_HINT, 0.85),
        (re.compile(r"(?i)\b(\d+[\d,]*\s*(dau|mau|qps|rps|tps|users|req/s|req/sec|requests per second|concurrent))\b"), EvidenceClassification.WORKLOAD_METRIC, 0.95),
    ]

    for loc, line in lines:
        stripped = line.strip()
        if not stripped or len(stripped) < 10 or stripped.startswith("#"):
            continue

        matched_class = EvidenceClassification.GENERAL_CONTEXT
        conf = 0.5
        for pattern, classification, confidence in req_patterns:
            if pattern.search(stripped):
                matched_class = classification
                conf = confidence
                break

        if matched_class != EvidenceClassification.GENERAL_CONTEXT:
            evidence.append(
                ExtractedEvidence(
                    evidence_id=f"EVID-{idx:04d}",
                    source_document=source_name,
                    file_name=os.path.basename(source_name),
                    document_type=doc_type,
                    section_or_location=loc,
                    content=stripped[:300],
                    evidence_classification=matched_class,
                    confidence=conf,
                )
            )
            idx += 1

    return evidence


class PlainTextParser(BaseDocumentParser):
    """Parser for raw plain text files (.txt)."""

    def can_parse(self, doc_format: DocumentFormat) -> bool:
        return doc_format == DocumentFormat.TXT

    def parse(self, file_path: Path, max_bytes: int = 20 * 1024 * 1024) -> IngestedDocument:
        fname = file_path.name
        try:
            raw_bytes = file_path.read_bytes()
            if len(raw_bytes) > max_bytes:
                return IngestedDocument(
                    file_path=str(file_path),
                    file_name=fname,
                    detected_format=DocumentFormat.TXT,
                    status=ExtractionStatus.EXCEEDS_SIZE_LIMIT,
                    error_message=f"File size ({len(raw_bytes)} bytes) exceeds limit ({max_bytes} bytes).",
                )

            # Decode with fallback
            for enc in ("utf-8", "utf-8-sig", "latin-1", "cp1252"):
                try:
                    text = raw_bytes.decode(enc)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                text = raw_bytes.decode("utf-8", errors="replace")

            normalized = _normalize_text(text)
            lines = [(f"Line {i}", l) for i, l in enumerate(normalized.splitlines(), 1)]
            evidence = _extract_evidence_from_lines(lines, str(file_path), "txt")

            return IngestedDocument(
                file_path=str(file_path),
                file_name=fname,
                detected_format=DocumentFormat.TXT,
                status=ExtractionStatus.SUCCESS,
                raw_text=normalized,
                metadata={
                    "byte_size": len(raw_bytes),
                    "line_count": len(lines),
                    "encoding": "utf-8",
                },
                evidence_items=evidence,
            )
        except Exception as e:
            return IngestedDocument(
                file_path=str(file_path),
                file_name=fname,
                detected_format=DocumentFormat.TXT,
                status=ExtractionStatus.ERROR,
                error_message=f"Failed to read text file: {e}",
            )


class MarkdownParser(BaseDocumentParser):
    """Parser for Markdown documentation (.md, .markdown)."""

    def can_parse(self, doc_format: DocumentFormat) -> bool:
        return doc_format == DocumentFormat.MARKDOWN

    def parse(self, file_path: Path, max_bytes: int = 20 * 1024 * 1024) -> IngestedDocument:
        fname = file_path.name
        try:
            raw_bytes = file_path.read_bytes()
            if len(raw_bytes) > max_bytes:
                return IngestedDocument(
                    file_path=str(file_path),
                    file_name=fname,
                    detected_format=DocumentFormat.MARKDOWN,
                    status=ExtractionStatus.EXCEEDS_SIZE_LIMIT,
                    error_message=f"File size exceeds limit ({max_bytes} bytes).",
                )

            text = raw_bytes.decode("utf-8", errors="replace")
            normalized = _normalize_text(text)

            headings: List[Dict[str, Any]] = []
            current_section = "Document Header"
            line_pairs: List[Tuple[str, str]] = []

            for i, line in enumerate(normalized.splitlines(), 1):
                h_match = re.match(r"^(#{1,6})\s+(.+)$", line.strip())
                if h_match:
                    level = len(h_match.group(1))
                    title = h_match.group(2).strip()
                    current_section = f"Section: {title}"
                    headings.append({"level": level, "title": title, "line": i})
                line_pairs.append((f"{current_section} (Line {i})", line))

            evidence = _extract_evidence_from_lines(line_pairs, str(file_path), "markdown")

            return IngestedDocument(
                file_path=str(file_path),
                file_name=fname,
                detected_format=DocumentFormat.MARKDOWN,
                status=ExtractionStatus.SUCCESS,
                raw_text=normalized,
                metadata={
                    "byte_size": len(raw_bytes),
                    "line_count": len(line_pairs),
                    "headings": headings,
                },
                evidence_items=evidence,
            )
        except Exception as e:
            return IngestedDocument(
                file_path=str(file_path),
                file_name=fname,
                detected_format=DocumentFormat.MARKDOWN,
                status=ExtractionStatus.ERROR,
                error_message=f"Failed to parse markdown: {e}",
            )


class CsvParser(BaseDocumentParser):
    """Parser for Comma-Separated Values structured data (.csv)."""

    def can_parse(self, doc_format: DocumentFormat) -> bool:
        return doc_format == DocumentFormat.CSV

    def parse(self, file_path: Path, max_bytes: int = 20 * 1024 * 1024) -> IngestedDocument:
        fname = file_path.name
        try:
            raw_bytes = file_path.read_bytes()
            if len(raw_bytes) > max_bytes:
                return IngestedDocument(
                    file_path=str(file_path),
                    file_name=fname,
                    detected_format=DocumentFormat.CSV,
                    status=ExtractionStatus.EXCEEDS_SIZE_LIMIT,
                    error_message=f"File size exceeds limit ({max_bytes} bytes).",
                )

            text = raw_bytes.decode("utf-8", errors="replace")
            normalized = _normalize_text(text)

            reader = csv.reader(io.StringIO(normalized))
            rows = list(reader)
            if not rows:
                return IngestedDocument(
                    file_path=str(file_path),
                    file_name=fname,
                    detected_format=DocumentFormat.CSV,
                    status=ExtractionStatus.PARTIAL,
                    raw_text="",
                    structured_data=[],
                    metadata={"row_count": 0, "column_count": 0},
                    warnings=["CSV file is empty."],
                )

            headers = [h.strip() for h in rows[0]]
            data_rows = rows[1:]

            # Evidence from schema headers
            evidence: List[ExtractedEvidence] = []
            if headers:
                evidence.append(
                    ExtractedEvidence(
                        evidence_id="EVID-CSV-SCHEMA-001",
                        source_document=str(file_path),
                        file_name=fname,
                        document_type="csv",
                        section_or_location="Header Row",
                        content=f"Columns: {', '.join(headers[:15])}",
                        evidence_classification=EvidenceClassification.DATA_SCHEMA,
                        confidence=0.90,
                        metadata={"columns": headers},
                    )
                )

            # Sample rows as structured records
            structured_records: List[Dict[str, str]] = []
            for r_idx, row in enumerate(data_rows[:100], 2):
                record = {headers[i] if i < len(headers) else f"col_{i}": val.strip() for i, val in enumerate(row)}
                structured_records.append(record)

            return IngestedDocument(
                file_path=str(file_path),
                file_name=fname,
                detected_format=DocumentFormat.CSV,
                status=ExtractionStatus.SUCCESS,
                raw_text=normalized[:10000],  # preview
                structured_data=structured_records,
                metadata={
                    "byte_size": len(raw_bytes),
                    "total_rows": len(rows),
                    "row_count": len(rows),
                    "column_count": len(headers),
                    "headers": headers,
                },
                evidence_items=evidence,
            )
        except Exception as e:
            return IngestedDocument(
                file_path=str(file_path),
                file_name=fname,
                detected_format=DocumentFormat.CSV,
                status=ExtractionStatus.ERROR,
                error_message=f"Failed to parse CSV: {e}",
            )


class DocxParser(BaseDocumentParser):
    """Parser for Microsoft Word documents (.docx) using optional python-docx."""

    def can_parse(self, doc_format: DocumentFormat) -> bool:
        return doc_format == DocumentFormat.DOCX

    def parse(self, file_path: Path, max_bytes: int = 20 * 1024 * 1024) -> IngestedDocument:
        fname = file_path.name
        try:
            import docx
        except ImportError:
            return IngestedDocument(
                file_path=str(file_path),
                file_name=fname,
                detected_format=DocumentFormat.DOCX,
                status=ExtractionStatus.MISSING_DEPENDENCY,
                error_message=(
                    "Optional dependency 'python-docx' is required to parse DOCX documents. "
                    "Install with: pip install python-docx"
                ),
            )

        try:
            if file_path.stat().st_size > max_bytes:
                return IngestedDocument(
                    file_path=str(file_path),
                    file_name=fname,
                    detected_format=DocumentFormat.DOCX,
                    status=ExtractionStatus.EXCEEDS_SIZE_LIMIT,
                    error_message=f"File size exceeds limit ({max_bytes} bytes).",
                )

            doc = docx.Document(str(file_path))
            paragraphs = []
            line_pairs: List[Tuple[str, str]] = []
            current_section = "Document Body"

            for p_idx, p in enumerate(doc.paragraphs, 1):
                p_text = p.text.strip()
                if not p_text:
                    continue
                if p.style and p.style.name.startswith("Heading"):
                    current_section = f"Section: {p_text}"
                paragraphs.append(p_text)
                line_pairs.append((f"{current_section} (Para {p_idx})", p_text))

            # Extract table cells
            table_count = len(doc.tables)
            table_texts: List[str] = []
            for t_idx, table in enumerate(doc.tables, 1):
                for r_idx, row in enumerate(table.rows):
                    row_vals = [c.text.strip() for c in row.cells if c.text.strip()]
                    if row_vals:
                        row_line = " | ".join(row_vals)
                        table_texts.append(row_line)
                        line_pairs.append((f"Table {t_idx} Row {r_idx}", row_line))

            all_text_parts = paragraphs + table_texts
            full_text = "\n\n".join(all_text_parts)
            normalized = _normalize_text(full_text)
            evidence = _extract_evidence_from_lines(line_pairs, str(file_path), "docx")

            # Extract core properties metadata
            meta: Dict[str, Any] = {
                "paragraph_count": len(paragraphs),
                "table_count": table_count,
            }
            try:
                cp = doc.core_properties
                if cp.title:
                    meta["title"] = cp.title
                if cp.author:
                    meta["author"] = cp.author
                if cp.created:
                    meta["created"] = str(cp.created)
            except Exception:
                pass

            return IngestedDocument(
                file_path=str(file_path),
                file_name=fname,
                detected_format=DocumentFormat.DOCX,
                status=ExtractionStatus.SUCCESS,
                raw_text=normalized,
                metadata=meta,
                evidence_items=evidence,
            )
        except Exception as e:
            return IngestedDocument(
                file_path=str(file_path),
                file_name=fname,
                detected_format=DocumentFormat.DOCX,
                status=ExtractionStatus.CORRUPTED if "not a valid" in str(e).lower() or "bad zip" in str(e).lower() else ExtractionStatus.ERROR,
                error_message=f"Failed to parse DOCX document: {e}",
            )


class PdfParser(BaseDocumentParser):
    """Parser for Adobe PDF documents (.pdf) using optional pypdf."""

    def can_parse(self, doc_format: DocumentFormat) -> bool:
        return doc_format == DocumentFormat.PDF

    def parse(self, file_path: Path, max_bytes: int = 20 * 1024 * 1024) -> IngestedDocument:
        fname = file_path.name
        try:
            # pyrefly: ignore[missing-import]
            import pypdf
        except ImportError:
            return IngestedDocument(
                file_path=str(file_path),
                file_name=fname,
                detected_format=DocumentFormat.PDF,
                status=ExtractionStatus.MISSING_DEPENDENCY,
                error_message=(
                    "Optional dependency 'pypdf' is required to parse PDF documents. "
                    "Install with: pip install pypdf"
                ),
            )

        try:
            if file_path.stat().st_size > max_bytes:
                return IngestedDocument(
                    file_path=str(file_path),
                    file_name=fname,
                    detected_format=DocumentFormat.PDF,
                    status=ExtractionStatus.EXCEEDS_SIZE_LIMIT,
                    error_message=f"File size exceeds limit ({max_bytes} bytes).",
                )

            reader = pypdf.PdfReader(str(file_path))
            page_count = len(reader.pages)
            extracted_pages: List[str] = []
            line_pairs: List[Tuple[str, str]] = []

            for p_num, page in enumerate(reader.pages, 1):
                p_text = page.extract_text() or ""
                p_norm = _normalize_text(p_text)
                if p_norm:
                    extracted_pages.append(p_norm)
                    for line in p_norm.splitlines():
                        if line.strip():
                            line_pairs.append((f"Page {p_num}", line.strip()))

            full_text = "\n\n".join(extracted_pages)
            if not full_text.strip():
                return IngestedDocument(
                    file_path=str(file_path),
                    file_name=fname,
                    detected_format=DocumentFormat.PDF,
                    status=ExtractionStatus.SCANNED_PDF_NO_TEXT,
                    raw_text="",
                    metadata={"page_count": page_count, "is_scanned_or_image_only": True},
                    warnings=[
                        "PDF contains zero extractable text stream. "
                        "The document appears to be scanned or image-only. "
                        "Interpretation requires a configured multimodal vision model; local OCR was not executed."
                    ],
                )

            evidence = _extract_evidence_from_lines(line_pairs, str(file_path), "pdf")
            return IngestedDocument(
                file_path=str(file_path),
                file_name=fname,
                detected_format=DocumentFormat.PDF,
                status=ExtractionStatus.SUCCESS,
                raw_text=full_text,
                metadata={
                    "page_count": page_count,
                    "extracted_pages": len(extracted_pages),
                },
                evidence_items=evidence,
            )
        except Exception as e:
            return IngestedDocument(
                file_path=str(file_path),
                file_name=fname,
                detected_format=DocumentFormat.PDF,
                status=ExtractionStatus.CORRUPTED if "pdf" in str(e).lower() or "eof" in str(e).lower() else ExtractionStatus.ERROR,
                error_message=f"Failed to parse PDF document: {e}",
            )


class XlsxParser(BaseDocumentParser):
    """Parser for Excel spreadsheets (.xlsx, .xls) using optional openpyxl."""

    def can_parse(self, doc_format: DocumentFormat) -> bool:
        return doc_format == DocumentFormat.XLSX

    def parse(self, file_path: Path, max_bytes: int = 20 * 1024 * 1024) -> IngestedDocument:
        fname = file_path.name
        try:
            import openpyxl
        except ImportError:
            return IngestedDocument(
                file_path=str(file_path),
                file_name=fname,
                detected_format=DocumentFormat.XLSX,
                status=ExtractionStatus.MISSING_DEPENDENCY,
                error_message=(
                    "Optional dependency 'openpyxl' is required to parse Excel spreadsheets. "
                    "Install with: pip install openpyxl"
                ),
            )

        try:
            if file_path.stat().st_size > max_bytes:
                return IngestedDocument(
                    file_path=str(file_path),
                    file_name=fname,
                    detected_format=DocumentFormat.XLSX,
                    status=ExtractionStatus.EXCEEDS_SIZE_LIMIT,
                    error_message=f"File size exceeds limit ({max_bytes} bytes).",
                )

            wb = openpyxl.load_workbook(str(file_path), read_only=True, data_only=True)
            sheets_data: Dict[str, Any] = {}
            text_chunks: List[str] = []
            evidence: List[ExtractedEvidence] = []

            for sheet_name in wb.sheetnames[:10]:
                sheet = wb[sheet_name]
                rows = list(sheet.iter_rows(values_only=True))
                if not rows:
                    continue
                headers = [str(c).strip() for c in rows[0] if c is not None]
                sheets_data[sheet_name] = {
                    "headers": headers,
                    "row_count": len(rows),
                }
                text_chunks.append(f"Sheet: {sheet_name}\nHeaders: {', '.join(headers)}")
                if headers:
                    evidence.append(
                        ExtractedEvidence(
                            evidence_id=f"EVID-XLSX-{len(evidence)+1:03d}",
                            source_document=str(file_path),
                            file_name=fname,
                            document_type="xlsx",
                            section_or_location=f"Sheet: {sheet_name}",
                            content=f"Columns: {', '.join(headers[:12])}",
                            evidence_classification=EvidenceClassification.DATA_SCHEMA,
                            confidence=0.88,
                        )
                    )

            wb.close()
            return IngestedDocument(
                file_path=str(file_path),
                file_name=fname,
                detected_format=DocumentFormat.XLSX,
                status=ExtractionStatus.SUCCESS,
                raw_text="\n\n".join(text_chunks),
                structured_data=sheets_data,
                metadata={
                    "sheet_count": len(wb.sheetnames),
                    "sheet_names": wb.sheetnames,
                },
                evidence_items=evidence,
            )
        except Exception as e:
            return IngestedDocument(
                file_path=str(file_path),
                file_name=fname,
                detected_format=DocumentFormat.XLSX,
                status=ExtractionStatus.CORRUPTED if "zip" in str(e).lower() else ExtractionStatus.ERROR,
                error_message=f"Failed to parse Excel document: {e}",
            )


class ImageNoticeParser(BaseDocumentParser):
    """Handler for image formats (.png, .jpg, .jpeg, .webp, .gif)."""

    def can_parse(self, doc_format: DocumentFormat) -> bool:
        return doc_format == DocumentFormat.IMAGE

    def parse(self, file_path: Path, max_bytes: int = 20 * 1024 * 1024) -> IngestedDocument:
        fname = file_path.name
        sz = file_path.stat().st_size
        return IngestedDocument(
            file_path=str(file_path),
            file_name=fname,
            detected_format=DocumentFormat.IMAGE,
            status=ExtractionStatus.PARTIAL,
            raw_text="",
            metadata={"byte_size": sz, "requires_vision_model": True},
            warnings=[
                f"Image file '{fname}' detected ({sz} bytes). "
                "Interpretation requires a configured multimodal vision provider. "
                "Local OCR was not executed."
            ],
        )
