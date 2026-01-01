def min_edit_distance(str1, str2):
    """
    計算兩個字串之間的最小編輯距離 (Levenshtein Distance)
    :param str1: 來源字串
    :param str2: 目標字串
    :return: 最小編輯距離整數
    """
    m = len(str1)
    n = len(str2)

    # 建立一個 (m+1) x (n+1) 的表格，初始化為 0
    # dp[i][j] 代表 str1 的前 i 個字元轉換到 str2 的前 j 個字元的最小距離
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

    # 初始化第一欄 (將 str1 變為空字串需要刪除 i 次)
    for i in range(m + 1):
        dp[i][0] = i

    # 初始化第一列 (從空字串變為 str2 需要插入 j 次)
    for j in range(n + 1):
        dp[0][j] = j

    # 開始填表
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # 如果字元相同，不需要操作，距離等於左上角的值
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # 如果字元不同，取以下三種操作的最小值 + 1：
                # 1. 插入 (Insertion): dp[i][j-1]
                # 2. 刪除 (Deletion):  dp[i-1][j]
                # 3. 替換 (Substitution): dp[i-1][j-1]
                dp[i][j] = 1 + min(dp[i][j - 1],    # 插入
                                   dp[i - 1][j],    # 刪除
                                   dp[i - 1][j - 1] # 替換
                                   )

    # 表格右下角即為最終答案
    return dp[m][n]

# --- 測試範例 ---
if __name__ == "__main__":
    s1 = "kitten"
    s2 = "sitting"
    
    distance = min_edit_distance(s1, s2)
    print(f"'{s1}' 和 '{s2}' 的最小編輯距離為: {distance}")
    
    # 另一個測試
    s3 = "flaw"
    s4 = "lawn"
    print(f"'{s3}' 和 '{s4}' 的最小編輯距離為: {min_edit_distance(s3, s4)}")