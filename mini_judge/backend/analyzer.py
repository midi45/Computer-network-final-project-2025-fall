from typing import Dict, List, Optional
from collections import Counter

from .rules import apply_rules

# =====================================================
# Rule configuration table (default settings)
# =====================================================

RULE_CONFIG: Dict[str, bool] = {
    "full_width": True,
    "brackets": True,
    "quotes": True,
    "assignment_vs_comparison": True,
    "confusable": False,
}


class Hint:
    """Simple hint container for static analysis results."""

    def __init__(self, rule: str, message: str, detail: Optional[str] = None):
        self.rule = rule
        self.message = message
        self.detail = detail

    def to_dict(self) -> Dict[str, str]:
        payload = {
            "rule": self.rule,
            "message": self.message,
        }
        if self.detail is not None:
            payload["detail"] = self.detail
        return payload


# =====================================================
# Analyzer main entry
# =====================================================

def analyze_code(
    code: str,
    enabled_rules: Optional[List[str]] = None,
) -> Dict[str, object]:
    """
    Run static analysis rules against the submitted code.

    Parameters
    ----------
    code : str
        Source code to be analyzed.
    enabled_rules : Optional[List[str]]
        If provided, only rules listed here will be executed.
        If None, RULE_CONFIG will be used as the default rule switch table.

    Returns
    -------
    List[Dict[str, str]]
        List of hint dictionaries.
    """

    # Determine which rules are enabled for this run
    if enabled_rules is not None:
        enabled_rule_set = set(enabled_rules)
    else:
        enabled_rule_set = {rule for rule, on in RULE_CONFIG.items() if on}

    hints: List[Hint] = []

    # apply_rules is expected to yield dicts with at least a `rule` key
    for result in apply_rules(code):
        if not result:
            continue

        rule_id = result.get("rule")
        if rule_id not in enabled_rule_set:
            continue  # Skip disabled rules

        hints.append(Hint(**result))

    rule_stats = Counter(hint.rule for hint in hints)

    return {
        "hints": [hint.to_dict() for hint in hints],
        "stats": dict(rule_stats),
    }
