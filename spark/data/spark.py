from pyspark import SparkContext
from itertools import combinations
print ("HERE SPARK IS STARTING")

sc = SparkContext("spark://spark-master:7077", "Recommended Items")

data = sc.textFile("/tmp/data/access.log", 2)
data = data.distinct()

pairs = data.map(lambda line: line.split("\t"))

grouped = pairs.groupByKey() #groups the different pairs by key value so a specific key would map to the list of different values


grouped_pairs = grouped.flatMap(lambda items: [(items[0],pair) for pair in combinations(items[1],2)]) #have the user id map to the different pairs of items the user visited.
output = grouped_pairs.collect()

print ("\n\n\n---------------------------------------------")


print ("Outputting a user and the pairs of items viewed")
for user, items in output:
    print ("User: %s items: %s" % (user, items))

print ("---------------------------------------------\n\n\n")

pages = grouped_pairs.map(lambda z: (tuple(sorted(z[1])), 1))
output = pages.collect()
print ("\n\n\n---------------------------------------------")
print ("Outputting a pair of items and mapping it to the number 1")
for items, user in output:
    print ("Items: %s Users: %s" % (items, user))
print ("---------------------------------------------\n\n\n")
count = pages.reduceByKey(lambda x,y: x+y)
output = count.collect()
print ("\n\n\n---------------------------------------------")
print("Co-viewed items mapping to number of users")

for page_id, counts in output:
    print ("co-viewed items: %s were viewed %d times" % (page_id, counts))
print ("---------------------------------------------\n\n\n")

filtered = count.filter(lambda z: z[1] >= 3) #filters only where value>=3
output = filtered.collect()
print ("\n\n\n---------------------------------------------")
print("Results only including co-viewed items by more than 3 users")
total = 0
for page_id, counts in output:
    print ("co-viewed items: %s were viewed %d times" % (page_id, counts))
    total+=counts

print("Sum of the above views:", total)
print ("---------------------------------------------\n\n\n")

sc.stop()