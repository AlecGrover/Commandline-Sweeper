
ls = []
count = 0
row =0
for i in range(2):
    for j in range(2):
        count +=1
        ls.append([count, i, j])

print(ls)


cord = [pos for pos in ls if pos[0] == 3]
print(cord[0][1], cord[0][2])