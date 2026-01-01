from datetime import datetime
power2n = [None] * 10000
# 方法 1
def power2n_1(n):
    return 2**n

# 方法 2a：用遞迴
def power2n_2(n):
    if n == 0: return 1
    else: return power2n_2(n-1) + power2n_2(n-1)
    
    # power2n(n-1)+power2n(n-1)

# 方法2b：用遞迴
def power2n_2b(n):
    if n == 0: return 1
    else: return 2 * power2n_2b(n-1)
# 方法 3：用遞迴+查表
def power2n_3(n):
    power2n[0] = 1
    if not power2n[n] is None: return power2n[n]
    power2n[n] = power2n_3(n-1) + power2n_3(n-1)
    return power2n[n]


n = 40
startTime = datetime.now()
# print(f'power2n_1({n})={power2n_1(n)}')
# print(f'power2n_2({n})={power2n_2(n)}') 
# print(f'power2n_2b({n})={power2n_2b(n)}')
print(f'power2n_3({n})={power2n_3(n)}')
endTime = datetime.now()
seconds = endTime - startTime
print(f'time:{seconds}')