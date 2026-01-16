import unittest
import shutil
import os
from app.core.engine import RuleEngine, ActionType
from app.core.parser import HttpRequest

class TestComplexRules(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests/rules_complex"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)
        os.makedirs(os.path.join(self.test_dir, "global"))
        os.makedirs(os.path.join(self.test_dir, "services", "8080"))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_global_drop_service_accept(self):
        # Global Rule: Drop Everything
        with open(os.path.join(self.test_dir, "global", "drop_all.rule"), "w") as f:
            f.write("action.drop()")

        # Service Rule (Port 8080): Accept /safe
        with open(os.path.join(self.test_dir, "services", "8080", "allow_safe.rule"), "w") as f:
            f.write("if '/safe' in request.path: action.accept()")

        engine = RuleEngine(self.test_dir)

        # Request to 8080 /safe -> Should PASS (Service Accept > Global Drop)
        req_safe = HttpRequest(path="/safe", destination_port=8080)
        act = engine.evaluate(req_safe)
        self.assertEqual(act.type, ActionType.ACCEPT)

        # Request to 8080 /unsafe -> Should DROP (Global Drop applies)
        req_unsafe = HttpRequest(path="/unsafe", destination_port=8080)
        act = engine.evaluate(req_unsafe)
        self.assertEqual(act.type, ActionType.DROP)

        # Request to 9090 (No service rules) -> Should DROP (Global Drop)
        req_other = HttpRequest(path="/safe", destination_port=9090)
        act = engine.evaluate(req_other)
        self.assertEqual(act.type, ActionType.DROP)

    def test_regex_support(self):
        with open(os.path.join(self.test_dir, "global", "regex.rule"), "w") as f:
            f.write("if re.search(r'^/api/v\d+', request.path): action.mark('api')")

        engine = RuleEngine(self.test_dir)

        req = HttpRequest(path="/api/v1/users")
        act = engine.evaluate(req)
        self.assertIn("api", act.tags)

        req2 = HttpRequest(path="/home")
        act2 = engine.evaluate(req2)
        self.assertNotIn("api", act2.tags)

if __name__ == "__main__":
    unittest.main()
