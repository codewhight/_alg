import numpy as np
import random
import math

# 1. 定義損失函數 (Loss Function) - 也就是我們要最小化的目標
# 線性回歸的目標是讓 (預測值 - 真實值) 的平方誤差越小越好
def loss_function(p, x_data, y_data):
    w, b = p # p[0] 是斜率 w, p[1] 是截距 b
    total_error = 0
    
    # 計算所有點的誤差總和 (Mean Squared Error)
    # 這裡用向量運算加速： Error = mean((y - (wx + b))^2)
    y_pred = w * x_data + b
    error = np.mean((y_data - y_pred) ** 2)
    
    return error

# 2. 改良版爬山演算法 (Hill-Climbing)
#    特點: 多次隨機重啟、適應性步長、局部搜尋與跳脫策略
#    目標: 最小化 loss_function

def improved_hill_climbing(x_data, y_data,
                           n_restarts=10,
                           init_step=1.0,
                           shrink_factor=0.5,
                           min_step=1e-6,
                           max_iters=5000,
                           stagnation_tol=100):
    """執行改良的爬山演算法尋找參數 p = [w, b]

    參數:
      - n_restarts: 隨機重啟次數
      - init_step: 初始步長
      - shrink_factor: 當找不到改善時步長縮小比例
      - min_step: 當步長小於此值時停止
      - max_iters: 每次重啟的最大迭代步數
      - stagnation_tol: 在無改善時觸發隨機跳脫的次數閾值
    返回最佳參數 p
    """
    best_p = None
    best_loss = float('inf')

    print(f"開始改良爬山: restarts={n_restarts}, init_step={init_step}, shrink_factor={shrink_factor}")

    for r in range(n_restarts):
        # 隨機初始化參數 w, b (給定合理範圍)
        p = np.array([random.uniform(-5, 5), random.uniform(0, 15)])
        step = init_step
        current_loss = loss_function(p, x_data, y_data)

        # 紀錄該重啟的最佳
        local_iters = 0
        stagn = 0

        # 每次重啟執行局部搜尋
        while step > min_step and local_iters < max_iters:
            improved = False
            # 產生鄰居解 (包含四向與對角)
            neighbors = []
            for dx in (step, -step, 0):
                for dy in (step, -step, 0):
                    if dx == 0 and dy == 0:
                        continue
                    neighbors.append(p + np.array([dx, dy]))

            # 檢查鄰居是否有改善
            for cand in neighbors:
                cand_loss = loss_function(cand, x_data, y_data)
                if cand_loss < current_loss:
                    p = cand
                    current_loss = cand_loss
                    improved = True
                    break

            if improved:
                stagn = 0
            else:
                # 若無改善，縮小步長
                step *= shrink_factor
                stagn += 1

            # 若長期無改善，嘗試隨機跳脫
            if stagn >= stagnation_tol:
                # 隨機小幅跳動以逃離局部最小值
                jump = np.random.normal(scale=step * 5.0, size=2)
                p = p + jump
                current_loss = loss_function(p, x_data, y_data)
                stagn = 0

            local_iters += 1

        print(f"Restart {r+1}/{n_restarts}: final_loss={current_loss:.6f}, p={p}, iters={local_iters}, final_step={step:.6e}")

        if current_loss < best_loss:
            best_loss = current_loss
            best_p = p.copy()

    print(f"搜尋結束: best_loss={best_loss:.6f}, best_p={best_p}")
    return best_p


# --- 測試主程式 ---

if __name__ == '__main__':
    # 固定隨機種子以便重現結果
    np.random.seed(0)
    random.seed(0)

    # 1. 準備一些假資料 (模擬 y = 3x + 10 加上一點雜訊)
    x_train = np.linspace(0, 10, 20)
    y_train = 3 * x_train + 10 + np.random.normal(0, 1, 20) # 真實參數應該接近 w=3, b=10

    # 2. 執行改良版爬山演算法
    print("--- 開始執行改良爬山線性回歸 ---")
    final_p = improved_hill_climbing(x_train, y_train, n_restarts=12, init_step=1.0)

    print("-" * 40)
    print(f"最終結果參數: w={final_p[0]:.6f}, b={final_p[1]:.6f}")
    print("真實目標參數: w=3.000000, b=10.000000")
