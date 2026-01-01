import itertools

def print_truth_table_inputs(n):
    # 1. 自動產生標題 (A, B, C, D...)
    # chr(65) 是 'A'
    headers = [chr(65 + i) for i in range(n)]
    
    # 2. 列印標題列
    header_str = "\t".join(headers)
    print(f"{header_str}")
    print("-" * (n * 4)) # 分隔線

    # 3. 使用 itertools.product 產生數據
    # 這裡我們用 [False, True] 並轉成整數顯示 (int())，
    # 這樣你可以輕易切換成 True/False 文字顯示
    for values in itertools.product([0, 1], repeat=n):
        # 將 Tuple 中的每個數字轉成字串並用 Tab 分隔
        row_str = "\t".join(str(v) for v in values)
        print(row_str)

# 執行：產生 4 個變數的真值表輸入
print_truth_table_inputs(4)