import re

with open('tests/test_rule_management_api.py', 'r') as f:
    content = f.read()

content = content.replace("assert test_rule_path in data", "assert any(item['path'] == test_rule_path for item in data)")

with open('tests/test_rule_management_api.py', 'w') as f:
    f.write(content)
