from typing import Dict, Iterable, Optional

from .brackets import check_unbalanced_brackets
from .confusable import check_confusable_characters
from .full_width import check_full_width_symbols
from .quotes import check_unclosed_quotes
from .assignment_vs_comparison import check_conditional_assignment_mistake


from . import full_width
from . import brackets
from . import quotes
from . import confusable

RuleResult = Optional[Dict[str, str]]


def apply_rules(code: str) -> Iterable[RuleResult]:
    yield check_full_width_symbols(code)
    yield check_unbalanced_brackets(code)
    yield check_unclosed_quotes(code)
    yield check_confusable_characters(code)
    yield check_conditional_assignment_mistake(code)

# Rule registry for frontend / metadata usage
RULES = {
    "full_width": full_width,
    "brackets": brackets,
    "quotes": quotes,
    "confusable": confusable,
    "assignment_vs_comparison": assignment_vs_comparison,
}
