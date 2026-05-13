import unittest

from coordination_system import TeamCoordinationActivitySystem


class TeamCoordinationActivitySystemTests(unittest.TestCase):
    def setUp(self) -> None:
        self.system = TeamCoordinationActivitySystem()

    def test_create_update_and_complete_activity(self) -> None:
        created = self.system.create_activity("Draft release notes", "engineering", owner="Sam")
        self.assertEqual(created["status"], "planned")

        updated = self.system.update_activity(created["id"], status="in_progress")
        self.assertEqual(updated["status"], "in_progress")

        completed = self.system.complete_activity(created["id"])
        self.assertEqual(completed["status"], "completed")

    def test_filter_activities_by_function_status_and_owner(self) -> None:
        one = self.system.create_activity("Triage queue", "support", owner="Riley")
        two = self.system.create_activity("Plan campaign", "marketing", owner="Alex")
        self.system.update_activity(two["id"], status="blocked")

        support_only = self.system.list_activities(function="support")
        self.assertEqual([a["id"] for a in support_only], [one["id"]])

        blocked_only = self.system.list_activities(status="blocked")
        self.assertEqual([a["id"] for a in blocked_only], [two["id"]])

        alex_only = self.system.list_activities(owner="Alex")
        self.assertEqual([a["id"] for a in alex_only], [two["id"]])

    def test_summary_counts(self) -> None:
        self.system.create_activity("A", "operations")
        b = self.system.create_activity("B", "operations")
        c = self.system.create_activity("C", "design")
        self.system.update_activity(b["id"], status="in_progress")
        self.system.update_activity(c["id"], status="blocked")

        summary = self.system.summary()
        self.assertEqual(summary["total"], 3)
        self.assertEqual(summary["by_status"]["planned"], 1)
        self.assertEqual(summary["by_status"]["in_progress"], 1)
        self.assertEqual(summary["by_status"]["blocked"], 1)
        self.assertEqual(summary["by_function"]["operations"], 2)
        self.assertEqual(summary["by_function"]["design"], 1)

    def test_rejects_invalid_status(self) -> None:
        activity = self.system.create_activity("A", "finance")
        with self.assertRaises(ValueError):
            self.system.update_activity(activity["id"], status="unknown")


if __name__ == "__main__":
    unittest.main()
