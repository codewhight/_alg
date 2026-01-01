'''
習題：《狼、羊、甘藍菜》過河的問題

題目:有一個人帶著一匹狼、一頭羊和一棵甘藍菜打算過河到對岸去。他的船很小, 每次只能載兩個東西:

也就是 【人 + 狼】 【人 + 羊】, 或【人 + 甘藍菜】。

困難的地方是, 如果他先載了甘藍菜過去, 狼就會趁機把羊吃掉了。而如果他先把狼送過去, 羊也會趁他離開時把甘藍菜吃掉。 

請問：他應該怎麼樣做才能夠把這二種動物和甘藍菜都送到對岸呢? 請找出運送順序！

程式：請寫一個程式搜尋出這個問題的解答！

'''

obj =['人', '狼', '羊', '甘藍菜']
state = [0, 0, 0, 0]  # 0:左岸 1:右岸
goal = [1, 1, 1, 1] # 目標狀態
visited = set()  # 記錄已拜訪的狀態
path = []  # 紀錄路徑

def dead(state):
    # 狼和羊在一起, 人不在
    if state[1] == state[2] and state[0] != state[1]:
        return True
    # 羊和甘藍菜在一起, 人不在
    if state[2] == state[3] and state[0] != state[2]:
        return True
    return False

def move(state, partner):
    """嘗試把人和 partner (None 表示人獨自) 從目前岸移到另一岸，
    若動作不合法或 partner 不和人在同岸，回傳 None；否則回傳新的狀態清單。
    partner: None | 1 | 2 | 3
    """
    new_state = state[:]  # 複製目前狀態

    # 人必定移動
    new_state[0] = 1 - new_state[0]

    # 若 partner 為 None，表示人獨自過河
    if partner is None:
        return new_state

    # 檢查 partner 是否為合法索引
    if partner not in (1, 2, 3):
        return None

    # 只有當 partner 在與人同一岸時，才能一起過河
    if state[partner] != state[0]:
        return None

    # 移動 partner
    new_state[partner] = 1 - new_state[partner]
    return new_state


def dfs(current_state):
    # 若到達目標，返回 True
    if current_state == goal:
        return True

    # 嘗試所有可能的移動：人獨自，或帶狼/羊/甘藍菜
    for partner in (None, 1, 2, 3):
        new_state = move(current_state, partner)
        if new_state is None:
            continue

        # 避免進入被吃掉的狀態
        if dead(new_state):
            continue

        key = tuple(new_state)
        if key in visited:
            continue

        # 記錄走法（說明文字 + 狀態）
        direction = '右岸' if new_state[0] == 1 else '左岸'
        from_side = '左岸' if current_state[0] == 0 else '右岸'
        if partner is None:
            desc = f"人獨自從{from_side}到{direction}"
        else:
            desc = f"人帶{obj[partner]}從{from_side}到{direction}"

        visited.add(key)
        path.append((desc, new_state[:]))

        # 遞迴搜尋
        if dfs(new_state):
            return True

        # 回溯
        path.pop()
        visited.remove(key)

    return False


def state_str(s):
    left = [obj[i] for i, v in enumerate(s) if v == 0]
    right = [obj[i] for i, v in enumerate(s) if v == 1]
    return f"左岸: {left}  右岸: {right}"


def solve():
    visited.clear()
    path.clear()
    visited.add(tuple(state))

    if dfs(state):
        print("找到解答！路徑如下：\n")
        # 印出初始狀態
        print(f"初始狀態 -> {state_str(state)}\n")
        for i, (desc, s) in enumerate(path, start=1):
            print(f"Step {i}: {desc}  =>  {state_str(s)}")
    else:
        print("未找到解答。")


if __name__ == '__main__':
    solve()

    
