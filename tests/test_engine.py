import unittest
from app.core.engine import RuleEngine, ActionType
from app.core.parser import HttpRequest
import os

class TestRuleEngine(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests/rules_test"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_drop_rule(self):
        # Create a rule file
        with open(f"{self.test_dir}/drop.rule", "w") as f:
            f.write("if 'bad' in request.path: action.drop()")

        engine = RuleEngine(self.test_dir)

        req_bad = HttpRequest(path="/bad/path")
        act_bad = engine.evaluate(req_bad)
        self.assertEqual(act_bad.type, ActionType.DROP)

        req_good = HttpRequest(path="/good/path")
        act_good = engine.evaluate(req_good)
        self.assertEqual(act_good.type, ActionType.ACCEPT)

    def test_priority(self):
        # Rule 1: Drop
        with open(f"{self.test_dir}/1.rule", "w") as f:
            f.write("if 'conflict' in request.path: action.drop()")

        # Rule 2: Accept
        with open(f"{self.test_dir}/2.rule", "w") as f:
            f.write("if 'conflict' in request.path: action.accept()")

        engine = RuleEngine(self.test_dir)

        req = HttpRequest(path="/conflict")
        act = engine.evaluate(req)

        # Accept > Drop
        self.assertEqual(act.type, ActionType.ACCEPT)

    def test_mark(self):
        with open(f"{self.test_dir}/mark.rule", "w") as f:
            f.write("action.mark('suspicious')")

        engine = RuleEngine(self.test_dir)
        req = HttpRequest()
        act = engine.evaluate(req)

        self.assertIn('suspicious', act.tags)
        self.assertEqual(act.type, ActionType.ACCEPT) # Mark is neutral/accept

if __name__ == "__main__":
    unittest.main()
