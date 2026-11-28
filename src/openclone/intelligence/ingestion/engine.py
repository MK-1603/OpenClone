"""Document Ingestion Engine orchestrating format detection, parsing, and evidence extraction."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

from src.openclone.intelligence.ingestion.models import (
    DocumentFormat,
    EvidenceClassification,
    ExtractionStatus,
    ExtractedEvidence,
    IngestedDocument,
)
from src.openclone.intelligence.ingestion.parsers import (
    BaseDocumentParser,
    CsvParser,
    DocxParser,
    ImageNoticeParser,
    MarkdownParser,
    PdfParser,
    PlainTextParser,
    XlsxParser,
)

EXTENSION_MAP: Dict[str, DocumentFormat] = {
    ".txt": DocumentFormat.TXT,
    ".text": DocumentFormat.TXT,
    ".log": DocumentFormat.TXT,
    ".md": DocumentFormat.MARKDOWN,
    ".markdown": DocumentFormat.MARKDOWN,
    ".mdown": DocumentFormat.MARKDOWN,
    ".csv": DocumentFormat.CSV,
    ".tsv": DocumentFormat.CSV,
    ".pdf": DocumentFormat.PDF,
    ".docx": DocumentFormat.DOCX,
    ".xlsx": DocumentFormat.XLSX,
    ".xlsm": DocumentFormat.XLSX,
    ".xls": DocumentFormat.XLSX,
    ".png": DocumentFormat.IMAGE,
    ".jpg": DocumentFormat.IMAGE,
    ".jpeg": DocumentFormat.IMAGE,
    ".webp": DocumentFormat.IMAGE,
    ".gif": DocumentFormat.IMAGE,
}


class DocumentIngestionEngine:
    """Orchestrator for multi-format document ingestion and evidence extraction."""

    def __init__(self, max_file_size_bytes: int = 20 * 1024 * 1024):
        self.max_file_size_bytes = max_file_size_bytes
        self.parsers: List[BaseDocumentParser] = [
            PlainTextParser(),
            MarkdownParser(),
            CsvParser(),
            DocxParser(),
            PdfParser(),
            XlsxParser(),
            ImageNoticeParser(),
        ]

    def detect_format(self, file_path: Path) -> DocumentFormat:
        """Identify document format from file extension and magic byte inspection."""
        ext = file_path.suffix.lower()
        if ext in EXTENSION_MAP:
            return EXTENSION_MAP[ext]

        # Magic byte inspection for extensionless or ambiguously named files
        try:
            with open(file_path, "rb") as f:
                header = f.read(16)
                if header.startswith(b"%PDF-"):
                    return DocumentFormat.PDF
                if header.startswith(b"PK\x03\x04"):
                    # Zip-based format: could be docx or xlsx
                    return DocumentFormat.DOCX
                if header.startswith(b"\x89PNG\r\n\x1a\n") or header.startswith(b"\xff\xd8\xff"):
                    return DocumentFormat.IMAGE
        except Exception:
            pass

        return DocumentFormat.UNKNOWN

    def validate_file(self, file_path: Path) -> Optional[IngestedDocument]:
        """Validate file existence, safety, and size limits."""
        if not file_path.exists():
            return IngestedDocument(
                file_path=str(file_path),
                file_name=file_path.name,
                detected_format=DocumentFormat.UNKNOWN,
                status=ExtractionStatus.ERROR,
                error_message=f"File not found: {file_path}",
            )

        if not file_path.is_file():
            return IngestedDocument(
                file_path=str(file_path),
                file_name=file_path.name,
                detected_format=DocumentFormat.UNKNOWN,
                status=ExtractionStatus.ERROR,
                error_message=f"Target is not a regular file: {file_path}",
            )

        try:
            sz = file_path.stat().st_size
            if sz > self.max_file_size_bytes:
                return IngestedDocument(
                    file_path=str(file_path),
                    file_name=file_path.name,
                    detected_format=self.detect_format(file_path),
                    status=ExtractionStatus.EXCEEDS_SIZE_LIMIT,
                    metadata={"byte_size": sz},
                    error_message=(
                        f"File size ({sz} bytes) exceeds maximum configured limit "
                        f"({self.max_file_size_bytes} bytes)."
                    ),
                )
        except Exception as e:
            return IngestedDocument(
                file_path=str(file_path),
                file_name=file_path.name,
                detected_format=DocumentFormat.UNKNOWN,
                status=ExtractionStatus.ERROR,
                error_message=f"Cannot inspect file permissions: {e}",
            )

        return None

    def ingest_file(self, file_path: Union[str, Path]) -> IngestedDocument:
        """Ingest a single document file with format detection and error isolation."""
        p = Path(file_path).resolve()

        # Step 1: Validation
        invalid_doc = self.validate_file(p)
        if invalid_doc is not None:
            return invalid_doc

        # Step 2: Format Detection
        fmt = self.detect_format(p)
        if fmt == DocumentFormat.UNKNOWN:
            return IngestedDocument(
                file_path=str(p),
                file_name=p.name,
                detected_format=DocumentFormat.UNKNOWN,
                status=ExtractionStatus.UNSUPPORTED,
                error_message=f"Unsupported or unrecognized file format: '{p.suffix}'",
            )

        # Step 3: Dispatch to matching parser
        for parser in self.parsers:
            if parser.can_parse(fmt):
                try:
                    return parser.parse(p, max_bytes=self.max_file_size_bytes)
                except Exception as e:
                    return IngestedDocument(
                        file_path=str(p),
                        file_name=p.name,
                        detected_format=fmt,
                        status=ExtractionStatus.ERROR,
                        error_message=f"Parser failure during extraction: {e}",
                    )

        return IngestedDocument(
            file_path=str(p),
            file_name=p.name,
            detected_format=fmt,
            status=ExtractionStatus.UNSUPPORTED,
            error_message=f"No parser available for format: {fmt.value}",
        )

    def ingest_documents(self, file_paths: List[Union[str, Path]]) -> List[IngestedDocument]:
        """Batch ingest multiple document files."""
        results: List[IngestedDocument] = []
        for fp in file_paths:
            results.append(self.ingest_file(fp))
        return results

    def ingest_files(self, file_paths: List[Union[str, Path]]) -> List[IngestedDocument]:
        """Alias for ingest_documents."""
        return self.ingest_documents(file_paths)

    def extract_evidence(self, documents: List[IngestedDocument]) -> List[ExtractedEvidence]:
        """Extract all evidence items from a collection of ingested documents."""
        all_evidence: List[ExtractedEvidence] = []
        for doc in documents:
            all_evidence.extend(doc.evidence_items)
        return all_evidence

    def ingest_directory(
        self,
        directory: Union[str, Path],
        recursive: bool = True,
        supported_only: bool = True,
    ) -> List[IngestedDocument]:
        """Scan directory and ingest all matching document files."""
        d = Path(directory).resolve()
        if not d.exists() or not d.is_dir():
            return []

        pattern = "**/*" if recursive else "*"
        candidates: List[Path] = []
        for path in d.glob(pattern):
            if path.is_file():
                if any(part.startswith(".") for part in path.parts):
                    continue
                if supported_only and path.suffix.lower() not in EXTENSION_MAP:
                    continue
                candidates.append(path)

        return self.ingest_documents(sorted(candidates))

    def extract_evidence_summary(self, documents: List[IngestedDocument]) -> Dict[str, Any]:
        """Aggregate evidence items across all ingested documents."""
        all_evidence: List[ExtractedEvidence] = []
        format_breakdown: Dict[str, int] = {}
        status_breakdown: Dict[str, int] = {}

        for doc in documents:
            fmt_val = doc.detected_format.value
            format_breakdown[fmt_val] = format_breakdown.get(fmt_val, 0) + 1

            st_val = doc.status.value
            status_breakdown[st_val] = status_breakdown.get(st_val, 0) + 1

            all_evidence.extend(doc.evidence_items)

        return {
            "total_documents": len(documents),
            "total_evidence_items": len(all_evidence),
            "formats": format_breakdown,
            "statuses": status_breakdown,
            "evidence_items": [e.to_dict() for e in all_evidence],
        }
