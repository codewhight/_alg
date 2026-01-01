def f(x, y):
    return -1 * ( x*x -2*x + y*y +2*y - 8 )

def greedy(f, x, y, h = 0.001, max_test=1000):
    count = 0
    current_value = f(x, y) #初始值
    while count < max_test:
        
        # 嘗試往四個方向找
        next_positions = [
            (x + h, y),
            (x - h, y),
            (x, y + h),
            (x, y - h)
        ]
        next_value = current_value
        next_x, next_y = x, y

        moved = False # 標記這輪有沒有移動

        for nx, ny in next_positions:
            val = f(nx, ny)

            if val > next_value:
                next_value = val
                next_x, next_y = nx, ny
                moved = True
                break # 找到了就跳出 不用看剩下的方向
        

        if moved == False:
            break
        x, y = next_x, next_y
        count += 1
    return x, y, f(x, y)
