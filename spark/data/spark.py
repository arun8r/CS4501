from pyspark import SparkContext
from itertools import combinations
print ("HERE SPARK IS STARTING")

sc = SparkContext("spark://spark-master:7077", "Recommended Items")

data = sc.textFile("/tmp/data/access.log", 2)
data = data.distinct()

pairs = data.map(lambda line: line.split("\t"))

grouped = pairs.groupByKey() #groups the different pairs by key value so a specific key would map to the list of different values
grouped_pairs = grouped.flatMap(lambda items: [(items[0],pair) for pair in combinations(items[1],2)]) #have the user id map to the different pairs of items the user visited.

pages = grouped_pairs.map(lambda z: (tuple(sorted(z[1])), 1))
count = pages.reduceByKey(lambda x,y: x+y)
filtered = count.filter(lambda z: z[1] >= 3) #filters only where value>=3
output = filtered.collect()

print("Results from spark:\n")
total = 0
for page_id, count in output:
    print ("co-viewed items: %s were viewed %d times" % (page_id, count))
    total+=count

print("Sum of the above views:", total)


sc.stop()