"""Unit tests for Polyglot Manifest and DataModel Inspectors (Go, Java, and SQL Foreign Keys)."""
import tempfile
import unittest
from pathlib import Path

from src.openclone.reverse_engineering.inspectors import DataModelInspector, ManifestInspector


class TestPolyglotInspectors(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_go_mod_manifest_inspection(self):
        """Verify ManifestInspector parses Go go.mod modules and direct dependencies."""
        go_mod = self.root / "go.mod"
        go_mod.write_text(
            """module github.com/openclone/sample-app

go 1.22

require (
\tgithub.com/gin-gonic/gin v1.9.1
\tgorm.io/gorm v1.25.7
)
""",
            encoding="utf-8",
        )

        inspector = ManifestInspector(self.root)
        deps = inspector.inspect()

        self.assertEqual(len(deps), 2)
        gin_dep = next(d for d in deps if "gin" in d.name)
        self.assertEqual(gin_dep.ecosystem, "go")
        self.assertEqual(gin_dep.version_constraint, "v1.9.1")

    def test_maven_pom_xml_manifest_inspection(self):
        """Verify ManifestInspector parses Java pom.xml dependencies."""
        pom = self.root / "pom.xml"
        pom.write_text(
            """<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.openclone</groupId>
    <artifactId>sample-service</artifactId>
    <version>1.0.0</version>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>3.2.0</version>
        </dependency>
    </dependencies>
</project>
""",
            encoding="utf-8",
        )

        inspector = ManifestInspector(self.root)
        deps = inspector.inspect()

        self.assertEqual(len(deps), 1)
        spring_dep = deps[0]
        self.assertEqual(spring_dep.name, "org.springframework.boot:spring-boot-starter-web")
        self.assertEqual(spring_dep.ecosystem, "maven")
        self.assertEqual(spring_dep.version_constraint, "3.2.0")

    def test_sql_ddl_foreign_key_extraction(self):
        """Verify DataModelInspector extracts foreign keys and relationship targets."""
        schema_sql = self.root / "schema.sql"
        schema_sql.write_text(
            """CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) NOT NULL
);

CREATE TABLE orders (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    total_amount DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
""",
            encoding="utf-8",
        )

        inspector = DataModelInspector(self.root)
        entities = inspector.inspect([schema_sql])

        self.assertEqual(len(entities), 2)
        orders = next(e for e in entities if e.name == "orders")
        self.assertEqual(len(orders.foreign_keys), 1)
        fk = orders.foreign_keys[0]
        self.assertEqual(fk["column"], "user_id")
        self.assertEqual(fk["target_table"], "users")
        self.assertEqual(fk["target_column"], "id")


if __name__ == "__main__":
    unittest.main()
