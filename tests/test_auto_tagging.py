import unittest
import shutil
import os
from app.core.engine import RuleEngine, ActionType
from app.core.parser import HttpRequest

class TestAutoTagging(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests/rules_autotag"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_drop_auto_tag(self):
        rule_name = "block_bad_stuff"
        with open(os.path.join(self.test_dir, f"{rule_name}.rule"), "w") as f:
            f.write("action.drop()")

        engine = RuleEngine(self.test_dir)
        req = HttpRequest(path="/bad")
        act = engine.evaluate(req)

        self.assertEqual(act.type, ActionType.DROP)
        self.assertIn(rule_name, act.tags)
        print(f"Tags found: {act.tags}")

    def test_mark_manual(self):
        rule_name = "mark_sus"
        with open(os.path.join(self.test_dir, f"{rule_name}.rule"), "w") as f:
            f.write("action.mark('suspicious')")

        engine = RuleEngine(self.test_dir)
        req = HttpRequest()
        act = engine.evaluate(req)

        self.assertIn("suspicious", act.tags)
        # Note: Rule name is NOT auto-added on mark() by default unless we decide to.
        # Requirement says "If rule drops... automatically mark".
        # "Just marked... marked with what is noted in action.mark('here')".
        # So manual mark doesn't enforce rule name tag, only Drop does.
        self.assertNotIn(rule_name, act.tags)

if __name__ == "__main__":
    unittest.main()
