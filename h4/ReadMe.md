了解 python 的 itertools 怎麼用
與AI的對話:https://gemini.google.com/share/cbf664c8620e
何謂itertools
簡單來說，itertools 是 Python 標準函式庫中的一個模組，專門用來處理 迭代器 (Iterators)。

主要用途
1.無限迭代器 (Infinite Iterators)
    會產生無限長的序列，通常需要搭配 break 或 islice 來停止，否則會跑進無窮迴圈。

2.排列組合迭代器 (Combinatoric Iterators)
    這是 itertools 最強大的功能之一，專門用來解決數學上的排列組合問題。

3.處理輸入序列的工具 (Terminating Iterators)
    這些工具用來操作已有的 List 或序列。

itertools 的應用
    1.需要「窮舉」所有可能性（暴力破解、排列組合）。
    2.需要處理「非常大」的檔案或資料流（記憶體優化）。
    3.想要消除醜陋的「多層巢狀迴圈」（程式碼美化）。
    4.需要對資料進行「分批」或「分組」操作。

核心邏輯(惰性求值)
itertools.count(1) 時，它並沒有產生任何數字存放在記憶體裡。它只記住了兩個資訊：

現在的公式（從 1 開始，每次 +1）。

目前的狀態（現在數到哪了）。

只有當呼叫 next()時，它才會透過 CPU 運算，「即時製造」出下一個數字給你，然後立刻暫停，等待下一次呼叫。

惰性求值就是 用時間換取空間 只做必要工作


實作
code_1:使用 itertools.product（笛卡兒積）顯示結果 
