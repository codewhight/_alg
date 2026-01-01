from flask import Flask, jsonify, request, send_from_directory, abort
from dataclasses import dataclass, field
from typing import List
import random
import threading
import os
from collections import deque

app = Flask(__name__)
lock = threading.Lock()

# 遊戲難度設定：列數 (r), 行數 (c), 地雷數 (m)
diffs = {
    'easy': {'r': 9, 'c': 9, 'm': 10},
    'medium': {'r': 16, 'c': 16, 'm': 40},
    'hard': {'r': 16, 'c': 30, 'm': 99}
}



@dataclass
class Cell:
    index: int          # 格子編號 (0 ~ N-1)
    row: int            # 列
    col: int            # 行
    isMine: bool = False      # 是否是地雷
    revealed: bool = False    # 是否已被翻開
    flagged: bool = False     # 是否被插旗
    adjacent: int = 0         # 周圍有多少顆地雷

@dataclass
class Game:
    
    rows: int = 9
    cols: int = 9
    mines: int = 10
    cells: List[Cell] = field(default_factory=list) # 儲存所有格子的清單
    started: bool = False       # 遊戲是否已開始
    gameOver: bool = False      # 遊戲是否結束
    flags: int = 0              # 已使用的旗幟數量
    revealedCount: int = 0      # 已翻開的格子數量

    def init_grid(self):
        #重置所有狀態
        # 根據行列數建立空白的格子列表
        self.cells = [Cell(index=i, row=i // self.cols, col=i % self.cols) for i in range(self.rows * self.cols)]
        self.started = False
        self.gameOver = False
        self.flags = 0
        self.revealedCount = 0

    def place_mines(self, first_index=-1):
        #隨機佈置地雷 排除玩家第一次點擊的位置 
        available = [i for i in range(len(self.cells)) if i != first_index]
        random.shuffle(available)
        
        for idx in available[:self.mines]:
            self.cells[idx].isMine = True
        
        for cell in self.cells:
            if cell.isMine:
                continue
            # 計算鄰居中有多少是地雷
            cell.adjacent = sum(1 for n in self.neighbors(cell.row, cell.col) if self.cells[n].isMine)

    def neighbors(self, r, c):
        #周圍鄰居
        arr = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0: continue # 跳過自己
                nr, nc = r + dr, c + dc
                # 檢查邊界，確保沒有超出網格範圍
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    arr.append(nr * self.cols + nc)
        return arr

    def reveal(self, index):
        #點擊格子時的邏輯 
        if self.gameOver: return
        cell = self.cells[index]
        
        # 已插旗或已翻開
        if cell.flagged or cell.revealed: return

        # 確保首點不死
        if not self.started:
            self.place_mines(index)
            self.started = True

        #遊戲結束
        if cell.isMine:
            cell.revealed = True
            self.gameOver = True
            self.reveal_all() # 顯示所有地雷
            return

        # 如果是空白 自動翻開周圍
        # 使用 deque 進行 BFS，以正確支援 popleft
        to_visit = deque([index])
        while to_visit:
            # 泛洪演算法 (Flood Fill) - DFS
            #i = to_visit.pop()
            # 泛洪演算法 (Flood Fill) - BFS
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

        # 檢查勝利條件：所有非地雷格子都已翻開
        if self.revealedCount >= len(self.cells) - self.mines:
            self.gameOver = True
            self.reveal_all() # 勝利時通常也會顯示全圖

    def flag(self, index):
        
        if self.gameOver: return
        cell = self.cells[index]
        if cell.revealed: return # 已翻開的不能插旗
        
        cell.flagged = not cell.flagged
        self.flags += 1 if cell.flagged else -1

    def reveal_all(self):
        
        for cell in self.cells:
            cell.revealed = True
        self.gameOver = True

    def serialize(self, show_mines=False):
        # 轉為JSON 格式回傳給前端
        out = []
        for cell in self.cells:
            d = {
                'index': cell.index,
                'revealed': cell.revealed,
                'flagged': cell.flagged,
                'adjacent': cell.adjacent
            }
            # 只有在作弊模式、遊戲結束或特定設定下才回傳「是否為地雷」，防止前端偷看
            if show_mines or self.gameOver:
                d['isMine'] = cell.isMine
            out.append(d)
        return out

# 建立一個全域的遊戲實例 (注意：這意味著所有連線的使用者都在玩同一盤遊戲)
game = Game()


#路由設定
@app.route('/minesweeper.html')
def serve_frontend():
    """ 傳送前端 HTML 檔案 """
    base_dir = os.path.dirname(__file__)
    return send_from_directory(base_dir, 'minesweeper.html')

@app.route('/api/new_game', methods=['POST'])
def api_new_game():
    """ API: 開始新遊戲 """
    data = request.get_json() or {}
    diff = data.get('difficulty', 'easy')
    if diff not in diffs:
        abort(400, 'unknown difficulty') # 錯誤請求
    
    with lock: # 確保線程安全
        settings = diffs[diff]
        game.rows = settings['r']
        game.cols = settings['c']
        game.mines = settings['m']
        game.init_grid()
    
    return jsonify({
        'rows': game.rows,
        'cols': game.cols,
        'mines': game.mines,
        'remaining_mines': game.mines - game.flags,
        'cells': game.serialize()
    })

@app.route('/api/state', methods=['GET'])
def api_state():
    """ API: 取得目前遊戲狀態 (例如重新整理頁面時) """
    with lock:
        return jsonify({
            'rows': game.rows,
            'cols': game.cols,
            'mines': game.mines,
            'remaining_mines': game.mines - game.flags,
            'gameOver': game.gameOver,
            'cells': game.serialize()
        })

@app.route('/api/reveal', methods=['POST'])
def api_reveal():
    """ API: 點擊/翻開格子 """
    data = request.get_json() or {}
    idx = data.get('index')
    if idx is None: abort(400, 'index required')
    
    try:
        idx = int(idx)
    except (TypeError, ValueError):
        abort(400, 'index must be an integer')
    with lock:
        if idx < 0 or idx >= len(game.cells):
            abort(400, 'index out of range')
        game.reveal(idx)
        return jsonify({
            'gameOver': game.gameOver,
            'message': 'revealed',
            'remaining_mines': game.mines - game.flags,
            'cells': game.serialize()
        })

@app.route('/api/flag', methods=['POST'])
def api_flag():
    """ API: 插旗動作 """
    data = request.get_json() or {}
    idx = data.get('index')
    if idx is None: abort(400, 'index required')
    
    try:
        idx = int(idx)
    except (TypeError, ValueError):
        abort(400, 'index must be an integer')
    with lock:
        if idx < 0 or idx >= len(game.cells):
            abort(400, 'index out of range')
        game.flag(idx)
        return jsonify({
            'remaining_mines': game.mines - game.flags,
            'cells': game.serialize()
        })

@app.route('/api/reveal_all', methods=['POST'])
def api_reveal_all():
    """ API: 作弊/放棄 (翻開全部)

    如果遊戲尚未開始，會隨機選一格作為「開始格」，並在佈雷時避開該格以保留第一次點擊的安全性。
    接著翻開所有格子並結束遊戲；回傳的 JSON 會包含被選為開始格的 index（若有的話）。
    """
    with lock:
        start_idx = None
        if not game.started:
            # 隨機選一格作為開始格，並在放置地雷時避開它
            start_idx = random.randrange(len(game.cells)) if len(game.cells) > 0 else None
            if start_idx is not None:
                game.place_mines(first_index=start_idx)
                game.started = True

        game.reveal_all()
        return jsonify({
            'gameOver': True,
            'startIndex': start_idx,
            'cells': game.serialize(show_mines=True)
        })

@app.route('/api/ping')
def api_ping():
    """ API: 測試伺服器是否活著 """
    return jsonify({'ok': True})


# 全域的未捕捉例外處理器：記錄詳細例外與回傳簡短錯誤訊息，方便除錯
from werkzeug.exceptions import HTTPException

@app.errorhandler(Exception)
def handle_unexpected_error(e):
    # 如果是 HTTPException（例如 abort(400)）就讓它原樣回傳，不轉成 500
    if isinstance(e, HTTPException):
        return e
    import traceback
    tb = traceback.format_exc()
    app.logger.exception('Unhandled exception: %s', e)
    # 回傳 minimal 的錯誤訊息給前端；完整 traceback 也會在 log 顯示
    return jsonify({'error': str(e), 'trace': tb}), 500


if __name__ == '__main__':
    # 啟動 Flask 伺服器，port 設定為 8000
    app.run(host='127.0.0.1', port=8000)