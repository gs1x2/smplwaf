import shutil
import os
import sys

sys.path.append(os.getcwd())
from app.core.engine import RuleEngine

def test_dynamic_creation():
    # 1. Setup: Create rules/ but DELETE rules/dynamic
    rules_dir = "tests/rules_test_dynamic"
    if os.path.exists(rules_dir):
        shutil.rmtree(rules_dir)
    os.makedirs(rules_dir) # Just root, no dynamic

    print(f"Created {rules_dir}, ensuring 'dynamic' is missing...")
    assert not os.path.exists(os.path.join(rules_dir, "dynamic"))

    # 2. Init Engine
    print("Initializing Engine...")
    engine = RuleEngine(rules_dir)

    # 3. Check dynamic dir exists now
    print("Checking for 'dynamic' dir...")
    if os.path.exists(os.path.join(rules_dir, "dynamic")):
        print("PASS: Dynamic directory created.")
    else:
        print("FAIL: Dynamic directory missing.")
        sys.exit(1)

    # 4. Try adding a rule
    print("Attempting to add rule...")
    success = engine.add_rule("test_rule", "pass")
    if success:
        print("PASS: Rule added successfully.")
    else:
        print("FAIL: Failed to add rule.")
        sys.exit(1)

    # Cleanup
    shutil.rmtree(rules_dir)

if __name__ == "__main__":
    test_dynamic_creation()
