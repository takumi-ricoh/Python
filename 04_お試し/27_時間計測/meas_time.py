# perfcounterのテスト

import time

start1 = time.perf_counter()
start2 = time.time()

for i in range(10**7):
    x = i

end1 = time.perf_counter()
end2 = time.time()

print(end1 - start1)
print(end2 - start2)
