import unittest
from pathlib import Path

from src.domain import NON_BYPASSABLE_SCENARIOS, REQUIRED_RECORDS, load_domain


class DomainTest(unittest.TestCase):
    def setUp(self):
        self.value = load_domain(Path("fixtures/domain.json"))

    def test_fixture_matches_domain(self):
        self.assertEqual(self.value["domain"], "maritime-rescue-transfer")
        self.assertGreaterEqual(self.value["version"], 2)
        self.assertGreaterEqual(len(self.value["constraints"]), 2)

    def test_closed_loop_records_present(self):
        # 证照、船员、预报、四类设备检查、缺陷复检、离港许可缺一不可
        self.assertTrue(REQUIRED_RECORDS.issubset(self.value["records"]))

    def test_non_bypassable_scenarios_present(self):
        # 换人、借设备、预报升级、转场、断网均不得绕过未关闭缺陷
        self.assertTrue(
            NON_BYPASSABLE_SCENARIOS.issubset(self.value["blocking_scenarios"])
        )

    def test_recheck_is_append_only_and_multi_agency_merges(self):
        text = "\n".join(self.value["constraints"])
        self.assertIn("只能追加", text)
        self.assertIn("归并", text)
        self.assertIn("责任", text)

    def test_release_and_escalation_and_feedback(self):
        text = "\n".join(self.value["constraints"])
        self.assertIn("证据", text)  # 值班员证据齐全才放行
        self.assertGreaterEqual(len(self.value["escalation"]), 2)
        self.assertTrue(self.value["feedback_loop"])


if __name__ == "__main__":
    unittest.main()
