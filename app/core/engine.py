from enum import Enum
from typing import Optional, Dict, Any, List
import logging
import os
import re # для правил
from app.core.parser import HttpRequest

logger = logging.getLogger(__name__)

class ActionType(Enum):
    ACCEPT = "ACCEPT"
    DROP = "DROP"
    MARK = "MARK"

class Action:
    def __init__(self, type: ActionType, tags: Optional[List[str]] = None):
        self.type = type
        self.tags = tags or []

    @classmethod
    def drop(cls):
        return cls(ActionType.DROP)

    @classmethod
    def accept(cls):
        return cls(ActionType.ACCEPT)

    @classmethod
    def mark(cls, tag: str):
        return cls(ActionType.MARK, [tag])

    def merge(self, other: 'Action'):
        new_tags = list(set(self.tags + other.tags))

        if self.type == ActionType.ACCEPT or other.type == ActionType.ACCEPT:
            return Action(ActionType.ACCEPT, new_tags)

        if self.type == ActionType.DROP or other.type == ActionType.DROP:
            return Action(ActionType.DROP, new_tags)

        return Action(ActionType.MARK, new_tags)

class RuleEngine:
    def __init__(self, rules_dir: str = "rules"):
        self.rules_dir = rules_dir
        self.rules = []
        self._load_rules()

    def _load_rules(self):
        self.rules = []
        if not os.path.exists(self.rules_dir):
            os.makedirs(self.rules_dir, exist_ok=True)

        os.makedirs(os.path.join(self.rules_dir, "dynamic"), exist_ok=True)



        for root, _, files in os.walk(self.rules_dir):
            for file in files:
                if file.endswith(".rule"):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r') as f:
                            code_str = f.read()
                            code = compile(code_str, path, 'exec')

                            rel_dir = os.path.relpath(root, self.rules_dir)
                            service_port = None

                            if rel_dir.startswith("services"):
                                try:
                                    parts = rel_dir.split(os.sep)
                                    if len(parts) >= 2:
                                        service_port = int(parts[1])
                                except:
                                    pass

                            self.rules.append({
                                'code': code,
                                'path': path,
                                'service_port': service_port
                            })
                    except Exception as e:
                        logger.error(f"Failed to load rule {path}: {e}")

    def reload_rules(self):
        logger.info("Reload rules...")
        self._load_rules()

    def add_rule(self, name: str, content: str):
        path = os.path.join(self.rules_dir, "dynamic", f"{name}.rule")
        try:
            with open(path, "w") as f:
                f.write(content)
            self.reload_rules()
            return True
        except Exception as e:
            logger.error(f"Failed to add rule {name}: {e}")
            return False

    def evaluate(self, request: HttpRequest) -> Action:
        final_action = Action(ActionType.MARK)

        class ActionContext:
            def __init__(self, rule_name: str):
                self.verdict = None
                self.tags = []
                self.rule_name = rule_name

            def drop(self):
                self.verdict = ActionType.DROP
                #пометка автоматическая дроп
                self.mark(self.rule_name) 

            def accept(self):
                self.verdict = ActionType.ACCEPT

            def mark(self, tag):
                self.tags.append(tag)

        global_verdict = None
        service_verdict = None
        all_tags = []

        for rule in self.rules:
            if rule['service_port'] is not None:
                if rule['service_port'] != request.destination_port:
                    continue 

            rule_name = os.path.splitext(os.path.basename(rule['path']))[0]
            ctx = ActionContext(rule_name)

            local_scope = {
                'request': request,
                'httprequest': request,
                'action': ctx,
                're': re
            }

            try:
                exec(rule['code'], {}, local_scope)

                if ctx.tags:
                    all_tags.extend(ctx.tags)

                if rule['service_port'] is not None:
                    if ctx.verdict == ActionType.ACCEPT:
                        service_verdict = ActionType.ACCEPT
                    elif ctx.verdict == ActionType.DROP:
                        if service_verdict != ActionType.ACCEPT:
                            service_verdict = ActionType.DROP
                else:
                    if ctx.verdict == ActionType.ACCEPT:
                        global_verdict = ActionType.ACCEPT
                    elif ctx.verdict == ActionType.DROP:
                        if global_verdict != ActionType.ACCEPT:
                            global_verdict = ActionType.DROP

            except Exception as e:
                logger.error(f"Error executing rule {rule['path']}: {e}")


        if service_verdict == ActionType.ACCEPT:
            return Action(ActionType.ACCEPT, list(set(all_tags)))

        if service_verdict == ActionType.DROP:
             return Action(ActionType.DROP, list(set(all_tags)))

        if global_verdict == ActionType.DROP:
            return Action(ActionType.DROP, list(set(all_tags)))

        return Action(ActionType.ACCEPT, list(set(all_tags)))
