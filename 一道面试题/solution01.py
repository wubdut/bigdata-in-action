import sys

dict = {}

for line in sys.stdin:
    line = line.strip()
    if dict.get(line) is None:
        dict[line] = 0
    dict[line] += 1

res = sorted(dict.items(), key=lambda d: d[1], reverse=True)

for i in range(10):
    print(i, res[i][0],res[i][1])

