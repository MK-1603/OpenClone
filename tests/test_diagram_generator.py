"""Unit tests for DiagramGenerator rendering valid Mermaid ER and C4 diagrams."""
import unittest

from src.openclone.reverse_engineering.diagrams import DiagramGenerator
from src.openclone.reverse_engineering.models import ApiEndpoint, EntityModel


class TestDiagramGenerator(unittest.TestCase):

    def test_generate_er_diagram_with_foreign_keys(self):
        """Verify Mermaid erDiagram contains valid relationship arrows and entity blocks."""
        users = EntityModel(
            name="users",
            columns=["id", "email", "name"],
            primary_key="id",
        )
        orders = EntityModel(
            name="orders",
            columns=["id", "user_id", "total"],
            primary_key="id",
            foreign_keys=[{"column": "user_id", "target_table": "users", "target_column": "id"}],
        )

        er_mermaid = DiagramGenerator.generate_er_diagram([users, orders])

        self.assertIn("erDiagram", er_mermaid)
        self.assertIn("USERS ||--o{ ORDERS : \"user_id\"", er_mermaid)
        self.assertIn("USERS {", er_mermaid)
        self.assertIn("string id PK", er_mermaid)
        self.assertIn("string email", er_mermaid)
        self.assertIn("ORDERS {", er_mermaid)

    def test_generate_c4_diagram(self):
        """Verify Mermaid C4 diagram structure."""
        endpoints = [ApiEndpoint(method="GET", path="/api/v1/orders", handler_name="get_orders")]
        entities = [EntityModel(name="orders", columns=["id"])]

        c4 = DiagramGenerator.generate_c4_diagram("OrderService", endpoints, entities)

        self.assertIn("C4Context", c4)
        self.assertIn("OrderService", c4)
        self.assertIn("Exposes 1 endpoints", c4)
        self.assertIn("Stores 1 persistent entities", c4)


if __name__ == "__main__":
    unittest.main()
