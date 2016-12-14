#nonSparkCount
#This is a program that tests our map-reduce using non-distributed computing

#task: number of distinct users who visited the same two products


products = {}
lines = [line.rstrip('\n') for line in open('access.log')]

for line in lines:
	loc = line.index("\t")
	userID = line[:loc]
	productID = int(line[loc+1:])

	if productID not in products:
		products[productID] = set()
	products[productID].add(userID)


print(products)


answers = {}

prod = sorted(list(products.keys()))
for i in range(len(prod)):
	key1 = prod[i]
	for j in range(i+1, len(prod)):
		key2 = prod[j]
		if key1 != key2:
			for user in products[key1]:
				if user in products[key2]:
					if (key1, key2) not in answers:
						answers[(key1, key2)] = 0
					answers[(key1, key2)] += 1

sortedAnswers = sorted(list(answers.keys()))
count = 0
for key in answers:
	if answers[key] >= 3:
		print("Products people viewed:", key, "Number of people who viewed both products:", answers[key])
		count = count + answers[key]
print(count)