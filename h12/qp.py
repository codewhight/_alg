import math
import random
import copy

# 1. 定義交叉熵函數 (User provided logic)
def cross_entropy(p, q):
    r = 0
    epsilon = 1e-15 # 防止 log(0) 錯誤
    for i in range(len(p)):
        # 限制 q[i] 最小值以避免數學錯誤
        q_val = max(q[i], epsilon)
        r += p[i] * math.log2(1 / q_val)
    return r

# 輔助函數：歸一化 (確保總和為 1)
def normalize(dist):
    total = sum(dist)
    return [x / total for x in dist]

# 爬山演算法
def hill_climbing_search(target_p, max_iterations=10000, step_size=0.01):
    dim = len(target_p)
    
    
    current_q = normalize([random.random() for _ in range(dim)])
    current_loss = cross_entropy(target_p, current_q)
    
    print(f"--- 開始爬山 ---")
    print(f"目標 P: {target_p}")
    print(f"初始 Q: {[round(x, 4) for x in current_q]}")
    print(f"初始 Loss: {current_loss:.6f}\n")
    
    for i in range(max_iterations):
        
        next_q_raw = []
        for val in current_q:
            noise = random.uniform(-step_size, step_size)
            # 確保數值不為負
            next_val = max(1e-10, val + noise) 
            next_q_raw.append(next_val)
            
        # 重新歸一化，使其符合機率定義
        next_q = normalize(next_q_raw)
        
        #計算新的 Loss
        next_loss = cross_entropy(target_p, next_q)
        
        # 如果新的解更好 (Loss 更低)，就移動過去 (爬向山谷底部)
        if next_loss < current_loss:
            current_q = next_q
            current_loss = next_loss
            
    return current_q, current_loss

#驗證 ---

# 設定一個固定的真實分佈 P
target_p = [0.1, 0.5, 0.4] 

# 執行算法
final_q, final_loss = hill_climbing_search(target_p)

print(f"--- 結果 ---")
print(f"目標 P (真值): {target_p}")
print(f"最終 Q (預測): {[round(x, 4) for x in final_q]}")
print(f"最終 Loss: {final_loss:.6f}")

# 驗證熵 (理論最小值)
entropy_p = cross_entropy(target_p, target_p)
print(f"理論最小值 H(p): {entropy_p:.6f}")

# 檢查誤差
diff = sum([abs(p - q) for p, q in zip(target_p, final_q)])
print(f"\n總絕對誤差 (|P-Q|): {diff:.6f}")
if diff < 0.01:
    print("驗證成功：演算法收斂至 Q ≈ P")
else:
    print("驗證未完全收斂，可能需要更多迭代")