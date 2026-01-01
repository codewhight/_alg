"""計算最小編輯距離 (Levenshtein distance)

用法:
  python min_edit_distance.py            # 內建範例
  python min_edit_distance.py str1 str2  # 輸出兩字串的距離
"""
from typing import List
import sys


def min_edit_distance(s1: str, s2: str) -> int:
    """回傳 s1 -> s2 的最小編輯距離（插入、刪除、替換，每步成本皆為 1）。"""
    m, n = len(s1), len(s2)
    # 使用 (m+1) x (n+1) 的 DP 表格
    dp: List[List[int]] = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j - 1],    # insert
                                   dp[i - 1][j],    # delete
                                   dp[i - 1][j - 1])  # replace
    return dp[m][n]


def _run_examples():
    examples = [
        ("kitten", "sitting", 3),
        ("flaw", "lawn", 2),
        ("", "abc", 3),
        ("abc", "abc", 0),
    ]

    for a, b, expect in examples:
        got = min_edit_distance(a, b)
        print(f"{a!r} -> {b!r}: distance = {got} (expected {expect})")
        assert got == expect
    print("All examples passed ✅")


if __name__ == '__main__':
    if len(sys.argv) == 3:
        a, b = sys.argv[1], sys.argv[2]
        print(min_edit_distance(a, b))
    else:
        _run_examples()
