total = list()
l = [[1],[2,3],[4]]
for x in l:
	for elem in x:
		total.append(elem)
print total
l = []
print [x for b in l for x in b]