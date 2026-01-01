import random

def monte(f, bounds, samples=100000):
    """
    使用蒙地卡羅法計算 n 維積分。
    
    參數:
    f: 目標函數 f(x_list)，接收一個座標列表，回傳數值。
    bounds: 積分範圍列表，例如 [(0, 1), (0, 1)] 代表 2 維。
    samples: 取樣點數 (越多越準，但越慢)。
    """
    
    # 計算積分範圍的「總體積」(Volume)
    # 對於 n 維來說，就是把每一維的長度乘起來
    volume = 1.0
    for lower, upper in bounds:
        dist = upper - lower
        volume *= dist
        
    # 隨機取樣並累加函數值
    total_value = 0.0
    
    for _ in range(samples):
        # 產生一個 n 維的隨機座標點
        # 走過所有bounds，對每一維產生一個該範圍內的隨機數
        current_coords = []
        for lower, upper in bounds:
            # random.uniform(lower, upper) 產生 a 到 b 之間的隨機浮點數
            r = random.uniform(lower, upper)
            current_coords.append(r)
        
        # 計算這個點的函數值，並加入總和
        total_value += f(current_coords)
    
    # 計算平均值並乘上體積
    # 積分值 = 體積 * (高度總和 / 點的數量)
    average_height = total_value / samples
    result = volume * average_height
    
    return result

#函式
def f(coords):
    x = coords[0]
    y = coords[1]
    return x**2 + y**2

#積分範圍
bounds = [(0, 1), (0, 1)]

# 設定取樣次數 (撒 50 萬個點)
N = 500000

print(f"正在進行 {len(bounds)} 維積分，取樣 {N} 次...")
estimated_result = monte(f, bounds, N)

print(f"蒙地卡羅計算結果: {estimated_result:.5f}")
