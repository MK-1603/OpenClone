"""Unit tests for OpenClone Reverse Engineering Intelligence Engine."""
import shutil
import tempfile
import unittest
from pathlib import Path

from src.openclone.reverse_engineering.engine import ReverseEngineeringEngine
from src.openclone.reverse_engineering.models import (
    ConfidenceLevel,
    CoverageStatus,
    ExecutionLevel,
)


class TestReverseEngineeringEngine(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.root = Path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_empty_repository(self):
        engine = ReverseEngineeringEngine(self.root)
        report = engine.analyze(ExecutionLevel.LEVEL_1_STATIC)

        self.assertEqual(report.total_files, 0)
        self.assertEqual(report.total_loc, 0)
        self.assertEqual(report.confidence, ConfidenceLevel.MEDIUM)
        self.assertEqual(len(report.dependencies), 0)
        self.assertEqual(len(report.symbols), 0)
        self.assertEqual(len(report.entities), 0)
        self.assertEqual(len(report.endpoints), 0)

    def test_level2_without_approval_raises_permission_error(self):
        engine = ReverseEngineeringEngine(self.root)
        with self.assertRaises(PermissionError):
            engine.analyze(ExecutionLevel.LEVEL_2_RUNTIME, human_approved=False)

    def test_polyglot_repository_static_analysis(self):
        # 1. Python file with complexity and API route
        py_file = self.root / "app.py"
        py_file.write_text(
            'from fastapi import FastAPI\n'
            'app = FastAPI()\n\n'
            '@app.get("/items")\n'
            'def get_items(limit: int = 10):\n'
            '    """Fetch items list."""\n'
            '    if limit > 100:\n'
            '        for i in range(10):\n'
            '            while limit > 1000:\n'
            '                try:\n'
            '                    with open("log") as f:\n'
            '                        pass\n'
            '                except Exception:\n'
            '                    pass\n'
            '    return []\n',
            encoding="utf-8",
        )

        # 2. SQL DDL file
        sql_file = self.root / "schema.sql"
        sql_file.write_text(
            'CREATE TABLE users (\n'
            '  id SERIAL PRIMARY KEY,\n'
            '  email VARCHAR(255) NOT NULL,\n'
            '  created_at TIMESTAMP\n'
            ');\n',
            encoding="utf-8",
        )

        # 3. pyproject.toml manifest
        pyproject = self.root / "pyproject.toml"
        pyproject.write_text(
            '[project]\n'
            'name = "testapp"\n'
            'dependencies = [\n'
            '  "fastapi>=0.100.0",\n'
            '  "uvicorn==0.22.0"\n'
            ']\n',
            encoding="utf-8",
        )

        # 4. package.json manifest
        pkg = self.root / "package.json"
        pkg.write_text(
            '{\n'
            '  "name": "frontend",\n'
            '  "dependencies": {\n'
            '    "react": "^18.2.0"\n'
            '  }\n'
            '}\n',
            encoding="utf-8",
        )

        engine = ReverseEngineeringEngine(self.root)
        report = engine.analyze(ExecutionLevel.LEVEL_1_STATIC)

        self.assertEqual(report.total_files, 4)
        self.assertTrue(report.total_loc > 20)
        self.assertIn("python", report.languages)
        self.assertIn("sql", report.languages)

        # Verify Dependencies
        dep_names = {d.name for d in report.dependencies}
        self.assertIn("fastapi", dep_names)
        self.assertIn("uvicorn", dep_names)
        self.assertIn("react", dep_names)

        # Verify Symbols & AST
        fn_symbols = [s for s in report.symbols if s.name == "get_items"]
        self.assertEqual(len(fn_symbols), 1)
        self.assertTrue(fn_symbols[0].complexity >= 5)

        # Verify SQL Entities
        self.assertEqual(len(report.entities), 1)
        self.assertEqual(report.entities[0].name, "users")
        self.assertEqual(report.entities[0].primary_key, "id")
        self.assertIn("email", report.entities[0].columns)

        # Verify API Endpoints
        self.assertEqual(len(report.endpoints), 1)
        self.assertEqual(report.endpoints[0].method, "GET")
        self.assertEqual(report.endpoints[0].path, "/items")
        self.assertEqual(report.endpoints[0].handler_name, "get_items")

        # Verify C4 Diagram
        self.assertIn("APIGateway", report.c4_diagram)
        self.assertIn("DataStore", report.c4_diagram)

        # Verify Coverage
        self.assertEqual(report.coverage.python_analysis, CoverageStatus.COMPLETE)
        self.assertEqual(report.coverage.sql_analysis, CoverageStatus.COMPLETE)
        self.assertEqual(report.coverage.dependency_analysis, CoverageStatus.COMPLETE)

        # Render Markdown Report
        md = engine.render_markdown_report(report)
        self.assertIn("# AS-IS ARCHITECTURE RECONSTRUCTION REPORT", md)
        self.assertIn("/items", md)
        self.assertIn("users", md)

    def test_security_secret_scanning(self):
        secret_file = self.root / "config.py"
        secret_file.write_text('AWS_KEY = "AKIAIOSFODNN7EXAMPLE"\n', encoding="utf-8")

        engine = ReverseEngineeringEngine(self.root)
        report = engine.analyze(ExecutionLevel.LEVEL_1_STATIC)

        self.assertEqual(len(report.security_findings), 1)
        self.assertEqual(report.security_findings[0].severity, "CRITICAL")
        self.assertTrue(report.security_findings[0].is_confirmed_vulnerability)
        self.assertIn("AWS Access Key", report.security_findings[0].description)


if __name__ == "__main__":
    unittest.main()
