期中專案遊戲 踩地雷 
製作部分:

遊戲介面由AI完成，再進行功能的修改
    功能說明:
        1.開始遊戲按鈕
        2.地圖(難易度)選擇
            9x9(10) , 16x16(40) , 16x30(99)
        3.顯示有幾顆地雷
        4.一次展開所有格子(開牌)
        5.重複遊玩按鈕

演算法部分主要由自己獨力完成 透過AI給予大致方向(主要是泛洪演算法部分)

使用到的演算法
# 泛洪演算法 (自動翻開周圍空白)
        to_visit = [index]
        while to_visit:
            i = to_visit.pop()
            c = self.cells[i]
            if c.revealed or c.flagged: continue
            
            c.revealed = True
            self.revealedCount += 1

# BFS (自動翻開周圍空白)
        to_visit = [index]
        while to_visit:
            #bfs
            i = to_visit.popleft()
            c = self.cells[i]
            if c.revealed or c.flagged: continue
            
            c.revealed = True
            self.revealedCount += 1
            
            # 如果周圍地雷數是 0，將鄰居加入待翻開清單
            if c.adjacent == 0:
                for n in self.neighbors(c.row, c.col):
                    if not self.cells[n].revealed and not self.cells[n].isMine:
                        to_visit.append(n)

# 隨機取樣 (放置地雷)
        available = [i for i in range(len(self.cells)) if i != first_index]
        random.shuffle(available)

# 網格遍歷 (計算某個格子周圍有幾顆地雷，以及在泛洪時找出周圍的格子)
        arr = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0: continue # 跳過自己
                nr, nc = r + dr, c + dc
                # 檢查邊界，確保沒有超出網格範圍
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    arr.append(nr * self.cols + nc)
        
