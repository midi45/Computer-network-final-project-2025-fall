import re
from typing import Dict, Optional

RULE_ID = "assignment_vs_comparison"
RULE_DESCRIPTION = "檢查在條件語句中誤用單等號賦值 (Check for assignment misusage in conditional statements)."

# 用於匹配註釋
COMMENT_PATTERN = re.compile(r"(\s*#.*)")

def check_conditional_assignment_mistake(code: str) -> Optional[Dict[str, str]]:
    lines = code.split('\n')
    
    for line_num, line in enumerate(lines):
        # 1. 移除行尾註釋，以避免註釋中的 '==' 誤導檢查
        # 這裡的處理方式是簡單地在第一個 # 處截斷，但更嚴謹的作法需要考慮 # 在字串內的情況。
        # 鑑於這是針對常見錯誤的 Linter，我們採用一種中間方案：
        code_part = line.split('#', 1)[0].strip()
        
        # 2. 檢查是否以條件關鍵字開頭 (if/while/elif)
        if re.match(r"^(if|while|elif)\b", code_part, re.IGNORECASE):
            
            # 3. 在移除註釋的部分中，尋找單個 '='
            # 我們需要一個更精確的正則表達式來匹配單獨的 `=` 符號
            # 排除 `==` 和 `:=` 的情況
            
            # 檢查是否存在單獨的賦值符號
            # r"(?<![=:])=(?!=)" 匹配前面不是 `=` 或 `:`，後面不是 `=` 的 `=` 
            if re.search(r"(?<![=:])=(?!=)", code_part):
                # 再次驗證：確保沒有比較運算符
                if '==' not in code_part and '!=' not in code_part and '<=' not in code_part and '>=' not in code_part:
                     return {
                        "rule": RULE_ID,
                        "message": "在條件語句中可能誤用了單等號 `=`。",
                        "detail": f"請檢查第 {line_num + 1} 行。單等號 `=` 是賦值，雙等號 `==` 才是比較。",
                    }
            
    return None
